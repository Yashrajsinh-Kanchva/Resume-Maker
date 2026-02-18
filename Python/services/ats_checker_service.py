"""
ATS Resume Score Checker Service
Analyzes resumes against job descriptions using NLP and ML techniques.
"""

import os
import tempfile
import re
from typing import Dict, List, Tuple, Optional
import pdfplumber
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import spacy
from openai import OpenAI
from utils.logger import setup_logger
from services.resume_score_service import _validate_resume_data

# Initialize logger
ats_logger = setup_logger(
    name="ATS_CHECKER",
    log_file="ats_checker.log"
)

# Load spaCy model (English)
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    ats_logger.warning("spaCy model 'en_core_web_sm' not found. Run: python -m spacy download en_core_web_sm")
    nlp = None

# Initialize OpenAI client
openai_client = None
if os.getenv("OPENAI_API_KEY"):
    openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Regex for extracting words (3+ letters) for tokenization/similarity
WORD_REGEX = r'\b[a-zA-Z]{3,}\b'

# Common stop words for word-overlap fallback
_STOP_WORDS = frozenset({
    'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'from',
    'as', 'is', 'are', 'was', 'were', 'been', 'be', 'have', 'has', 'had', 'do', 'does',
    'did', 'will', 'would', 'should', 'could', 'may', 'might', 'must', 'can', 'this',
    'that', 'these', 'those', 'a', 'an'
})


def _pick_final_similarity(tfidf_pct: float, overlap_pct: float) -> float:
    """Choose final similarity from TF-IDF and word-overlap percentages."""
    if tfidf_pct < 5.0 and overlap_pct > 5.0:
        return min(overlap_pct * 1.2, 80.0)
    if tfidf_pct < 0.1:
        return min(overlap_pct, 80.0)
    return max(tfidf_pct, overlap_pct * 0.9)


def _fallback_ats_suggestions(
    missing_keywords: List[str],
    formatting_issues: List[str],
    default_message: str,
    *,
    keyword_prefix: str = "Consider adding these keywords naturally in your experience section:",
    include_formatting_detail: bool = True
) -> List[str]:
    """Build suggestion list when OpenAI is unavailable or errors."""
    suggestions = []
    if missing_keywords:
        top = missing_keywords[:5]
        suggestions.append(f"{keyword_prefix} {', '.join(top)}")
    if formatting_issues and include_formatting_detail:
        if any("table" in issue.lower() for issue in formatting_issues):
            suggestions.append("Avoid using tables - ATS systems may not parse them correctly")
        if any("summary" in issue.lower() for issue in formatting_issues):
            suggestions.append("Add a professional summary section to improve ATS compatibility")
    if formatting_issues and not include_formatting_detail:
        suggestions.append("Fix formatting issues detected in your resume")
    return suggestions if suggestions else [default_message]


def _step1_parts(step1: Dict) -> List[str]:
    """Extract step1 (personal) fields into list of strings for resume text."""
    out = []
    if not step1:
        return out
    for key in ("name", "title", "summary", "email", "phone", "location"):
        val = step1.get(key)
        if val:
            out.append(val if isinstance(val, str) else str(val))
    return out


def _step4_skills_parts(step4) -> List[str]:
    """Extract step4 (skills) into list of strings."""
    out = []
    if not step4:
        return out
    if isinstance(step4, list):
        skills_list = []
        for s in step4:
            if not s:
                continue
            if isinstance(s, str):
                skills_list.append(s)
            elif isinstance(s, dict):
                skills_list.append(s.get("name", "") or "")
        if skills_list:
            out.append(" ".join(skills_list))
            out.append("Skills: " + ", ".join(skills_list))
    else:
        out.append(str(step4))
    return out


def _step2_education_parts(step2: Dict) -> List[str]:
    """Extract step2 (education) into list of strings."""
    out = []
    if not step2:
        return out
    edu_parts = []
    for key in ("degree", "field"):
        val = step2.get(key)
        if val:
            edu_parts.append(val)
            out.append(val)
    inst = step2.get("institution") or step2.get("school")
    if inst:
        edu_parts.append(inst)
        out.append(inst)
    if edu_parts:
        out.append(" ".join(edu_parts))
    return out


def _single_experience_parts(exp: Dict) -> List[str]:
    """Extract one experience entry into list of strings."""
    out = []
    job_title = exp.get("jobTitle")
    employer = exp.get("employer") or exp.get("company")
    exp_parts = [p for p in (job_title, employer) if p]
    if job_title:
        out.append(job_title)
    if employer:
        out.append(employer)
    if exp_parts:
        out.append(" ".join(exp_parts))
    if exp.get("description"):
        out.append(exp["description"])
    for key in ("startDate", "endDate"):
        val = exp.get(key)
        if val is not None:
            out.append(str(val))
    return out


def _step3_experience_parts(step3: List) -> List[str]:
    """Extract step3 (experience) into list of strings."""
    if not step3 or not isinstance(step3, list):
        return []
    out = []
    for exp in step3:
        if isinstance(exp, dict):
            out.extend(_single_experience_parts(exp))
    return out


def _step1_languages_parts(step1: Dict) -> List[str]:
    """Extract languages from step1."""
    out = []
    langs = step1.get("languages") if step1 else None
    if not langs:
        return out
    if isinstance(langs, list):
        out.append(" ".join(langs))
        out.append("Languages: " + ", ".join(langs))
    else:
        out.append(str(langs))
    return out


def _step1_certs_parts(step1: Dict) -> List[str]:
    """Extract certificates from step1."""
    out = []
    certs = (step1.get("certificates") or step1.get("certs")) if step1 else None
    if not certs:
        return out
    if isinstance(certs, list):
        out.append(" ".join(certs))
        out.append("Certifications: " + ", ".join(certs))
    else:
        out.append(str(certs))
    return out


def _custom_sections_parts(custom_sections: List) -> List[str]:
    """Extract custom sections into list of strings."""
    out = []
    if not custom_sections:
        return out
    for section in custom_sections:
        if not isinstance(section, dict):
            continue
        if section.get("name"):
            out.append(section["name"])
        if section.get("description"):
            out.append(section["description"])
    return out


class ATSCheckerService:
    """Service for ATS resume analysis and scoring."""
    
    def __init__(self):
        self.required_sections = ["skills", "experience", "education"]
        self.optional_sections = ["summary", "projects", "certifications", "languages"]
    
    def check_resume_from_data(self, resume_data: Dict, job_description: str) -> Dict:
        """
        Check resume using saved resume data (bypasses PDF parsing).
        
        Args:
            resume_data: Resume data dictionary with step1, step2, step3, step4, etc.
            job_description: Job description text
            
        Returns:
            Dictionary with ATS score and analysis results
        """
        try:
            # Build resume text from structured data
            resume_text = self._build_resume_text_from_data(resume_data)
            
            # Log the built resume text for debugging
            ats_logger.info("=== RESUME TEXT BUILDING ===")
            ats_logger.info(f"Resume text length: {len(resume_text)} characters")
            ats_logger.info(f"Resume text preview (first 500 chars): {resume_text[:500]}")
            ats_logger.info(f"Resume data keys: {list(resume_data.keys())}")
            
            if not resume_text or len(resume_text.strip()) < 50:
                ats_logger.error(f"Resume text is too short or empty. Length: {len(resume_text) if resume_text else 0}")
                return {
                    "error": "Resume data is incomplete or empty.",
                    "ats_score": 0
                }
            
            # Detect resume sections
            sections = self._detect_sections_from_data(resume_data)
            ats_logger.info(f"Detected sections: {sections}")
            
            # Extract keywords from resume and JD
            resume_keywords = self._extract_keywords(resume_text)
            jd_keywords = self._extract_keywords(job_description)
            
            ats_logger.info(f"Resume keywords extracted: {len(resume_keywords)} keywords")
            ats_logger.info(f"JD keywords extracted: {len(jd_keywords)} keywords")
            ats_logger.info(f"Sample resume keywords: {resume_keywords[:20]}")
            ats_logger.info(f"Sample JD keywords: {jd_keywords[:20]}")
            
            # Calculate keyword match percentage using TF-IDF cosine similarity
            ats_logger.info("=== CALCULATING KEYWORD SIMILARITY ===")
            print(f"[ATS] Calculating keyword similarity - Resume text length: {len(resume_text)}, JD length: {len(job_description)}")
            keyword_match_percent = self._calculate_keyword_similarity(
                resume_text, job_description
            )
            
            ats_logger.info(f"Final keyword_match_percent: {keyword_match_percent}")
            print(f"[ATS] Final keyword_match_percent: {keyword_match_percent}")
            
            # Ensure keyword_match_percent is valid
            if keyword_match_percent is None or keyword_match_percent < 0:
                ats_logger.warning("Invalid keyword_match_percent, setting to 0")
                keyword_match_percent = 0.0
            
            # Check formatting issues (minimal for data-based resumes)
            formatting_issues = []
            if not resume_data.get("step1", {}).get("summary"):
                formatting_issues.append("No summary section found")
            # Data quality: flag invalid/placeholder values (e.g. 11111 in name)
            try:
                data_warnings = _validate_resume_data(resume_data)
                for w in data_warnings:
                    formatting_issues.append(w)
            except Exception:
                pass
            
            # Calculate structure score
            structure_score = self._calculate_structure_score(sections)
            
            # Ensure structure_score is valid
            if structure_score is None or structure_score < 0:
                ats_logger.warning("Invalid structure_score, setting to 0")
                structure_score = 0.0
            
            # Calculate formatting score
            formatting_score = self._calculate_formatting_score(formatting_issues)
            
            # Ensure formatting_score is valid
            if formatting_score is None or formatting_score < 0:
                ats_logger.warning("Invalid formatting_score, setting to 0")
                formatting_score = 0.0
            
            # Calculate final ATS score
            ats_score = self._calculate_ats_score(
                keyword_match_percent,
                structure_score,
                formatting_score
            )
            
            # Debug logging to track score calculation
            ats_logger.info(f"ATS Score Calculation - Keyword Match: {keyword_match_percent:.1f}%, Structure: {structure_score:.1f}, Formatting: {formatting_score:.1f}, Final Score: {ats_score:.1f}")
            ats_logger.info(f"Sections detected: {sections}")
            ats_logger.info(f"Formatting issues: {formatting_issues}")
            ats_logger.info(f"Resume text length: {len(resume_text)}, JD length: {len(job_description)}")
            
            # Find missing keywords
            missing_keywords = self._find_missing_keywords(jd_keywords, resume_keywords)
            
            # Get AI suggestions (using OpenAI)
            ai_suggestions = self._get_ai_suggestions(
                resume_text, job_description, missing_keywords, formatting_issues
            )
            
            result = {
                "ats_score": round(ats_score, 1),
                "keyword_match_percent": round(keyword_match_percent, 1),
                "missing_keywords": missing_keywords[:10],  # Top 10 missing keywords
                "sections_found": sections,
                "formatting_issues": formatting_issues,
                "ai_suggestions": ai_suggestions,
                "structure_score": round(structure_score, 1),
                "formatting_score": round(formatting_score, 1)
            }
            
            # Log final result to verify it's not being modified
            ats_logger.info(f"Returning ATS result: ats_score={result['ats_score']}, keyword_match={result['keyword_match_percent']}, structure={result['structure_score']}, formatting={result['formatting_score']}")
            
            return result
            
        except Exception as e:
            ats_logger.error(f"Error checking resume from data: {str(e)}", exc_info=True)
            return {
                "error": f"Error processing resume: {str(e)}",
                "ats_score": 0
            }
    
    def check_resume(self, pdf_file, job_description: str) -> Dict:
        """
        Main method to check resume against job description.
        
        Args:
            pdf_file: Uploaded PDF file object
            job_description: Job description text
            
        Returns:
            Dictionary with ATS score and analysis results
        """
        temp_file_path = None
        try:
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                pdf_file.save(tmp_file.name)
                temp_file_path = tmp_file.name
            
            # Extract text from PDF
            resume_text = self._extract_text_from_pdf(temp_file_path)
            
            if not resume_text or len(resume_text.strip()) < 50:
                return {
                    "error": "Resume text could not be extracted from PDF. This often happens with image-based PDFs (like those downloaded from this site). Please use 'Use Saved Resume' option instead for more accurate analysis.",
                    "ats_score": 0
                }
            
            # Detect resume sections
            sections = self._detect_sections(resume_text)
            
            # Extract keywords from resume and JD
            resume_keywords = self._extract_keywords(resume_text)
            jd_keywords = self._extract_keywords(job_description)
            
            # Calculate keyword match percentage using TF-IDF cosine similarity
            keyword_match_percent = self._calculate_keyword_similarity(
                resume_text, job_description
            )
            
            # Check formatting issues
            formatting_issues = self._check_formatting_issues(temp_file_path, resume_text)
            
            # Calculate structure score
            structure_score = self._calculate_structure_score(sections)
            
            # Calculate formatting score
            formatting_score = self._calculate_formatting_score(formatting_issues)
            
            # Calculate final ATS score
            ats_score = self._calculate_ats_score(
                keyword_match_percent,
                structure_score,
                formatting_score
            )
            
            # Find missing keywords
            missing_keywords = self._find_missing_keywords(jd_keywords, resume_keywords)
            
            # Get AI suggestions (using OpenAI)
            ai_suggestions = self._get_ai_suggestions(
                resume_text, job_description, missing_keywords, formatting_issues
            )
            
            return {
                "ats_score": round(ats_score, 1),
                "keyword_match_percent": round(keyword_match_percent, 1),
                "missing_keywords": missing_keywords[:10],  # Top 10 missing keywords
                "sections_found": sections,
                "formatting_issues": formatting_issues,
                "ai_suggestions": ai_suggestions,
                "structure_score": round(structure_score, 1),
                "formatting_score": round(formatting_score, 1)
            }
            
        except Exception as e:
            ats_logger.error(f"Error checking resume: {str(e)}", exc_info=True)
            return {
                "error": f"Error processing resume: {str(e)}",
                "ats_score": 0
            }
        finally:
            # Cleanup: Delete temporary file
            if temp_file_path and os.path.exists(temp_file_path):
                try:
                    os.unlink(temp_file_path)
                except Exception as e:
                    ats_logger.warning(f"Failed to delete temp file: {e}")
    
    def _extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF file with OCR fallback for image-based PDFs."""
        try:
            text_parts = []
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text_parts.append(page_text)
            
            extracted_text = "\n".join(text_parts)
            
            # If text extraction failed or returned very little text, try OCR fallback
            # If text extraction failed or returned very little text, provide helpful error
            if not extracted_text or len(extracted_text.strip()) < 50:
                ats_logger.warning(f"PDF text extraction returned minimal text ({len(extracted_text) if extracted_text else 0} chars)")
                # Try OCR fallback (if available)
                ocr_text = self._extract_text_with_ocr(pdf_path)
                if ocr_text and len(ocr_text.strip()) >= 50:
                    extracted_text = ocr_text
                else:
                    # If OCR also fails, return empty to trigger error message
                    ats_logger.warning("OCR fallback also failed or not available")
                    return ""
            
            return extracted_text
        except Exception as e:
            ats_logger.error(f"Error extracting PDF text: {e}")
            # Try OCR as last resort
            try:
                return self._extract_text_with_ocr(pdf_path)
            except Exception as ocr_error:
                ats_logger.error(f"OCR fallback also failed: {ocr_error}")
                return ""
    
    def _extract_text_with_ocr(self, pdf_path: str) -> str:
        """Extract text from image-based PDF using OCR (pytesseract)."""
        try:
            # Try to import OCR libraries
            try:
                from pdf2image import convert_from_path
                import pytesseract
            except ImportError:
                ats_logger.warning("OCR libraries not installed. Install with: pip install pdf2image pytesseract")
                return ""
            
            # Convert PDF pages to images
            images = convert_from_path(pdf_path, dpi=200)
            
            # Extract text from each image using OCR
            text_parts = []
            for img in images:
                text = pytesseract.image_to_string(img)
                if text:
                    text_parts.append(text)
            
            return "\n".join(text_parts)
        except Exception as e:
            ats_logger.error(f"OCR extraction failed: {e}")
            return ""
    
    def _detect_sections(self, resume_text: str) -> Dict[str, bool]:
        """Detect resume sections based on common headers."""
        text_lower = resume_text.lower()
        
        sections = {
            "summary": False,
            "skills": False,
            "experience": False,
            "education": False,
            "projects": False,
            "certifications": False,
            "languages": False
        }
        
        # Common section header patterns
        section_patterns = {
            "summary": [
                r"\b(summary|objective|profile|about|overview)\b",
                r"career\s+objective",
                r"professional\s+summary"
            ],
            "skills": [
                r"\b(skills?|technical\s+skills?|core\s+skills?|competencies?)\b",
                r"key\s+skills"
            ],
            "experience": [
                r"\b(experience|work\s+experience|employment|work\s+history|professional\s+experience)\b",
                r"employment\s+history"
            ],
            "education": [
                r"\b(education|academic|qualifications?|degrees?)\b",
                r"educational\s+background"
            ],
            "projects": [
                r"\b(projects?|key\s+projects?|notable\s+projects?)\b"
            ],
            "certifications": [
                r"\b(certifications?|certificates?|credentials?)\b"
            ],
            "languages": [
                r"\b(languages?|language\s+proficiency)\b"
            ]
        }
        
        for section, patterns in section_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text_lower, re.IGNORECASE):
                    sections[section] = True
                    break
        
        return sections
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text using NLP."""
        if not nlp:
            # Fallback: simple word extraction
            words = re.findall(WORD_REGEX, text.lower())
            return list(set(words))
        
        doc = nlp(text.lower())
        keywords = []
        
        # Extract nouns, proper nouns, and important terms
        for token in doc:
            if (token.pos_ in ["NOUN", "PROPN"] and 
                not token.is_stop and 
                not token.is_punct and
                len(token.text) > 2):
                keywords.append(token.text.lower())
        
        # Also extract noun phrases
        for chunk in doc.noun_chunks:
            if len(chunk.text.split()) <= 3:  # Max 3-word phrases
                keywords.append(chunk.text.lower().strip())
        
        return list(set(keywords))
    
    def _calculate_keyword_similarity(self, resume_text: str, jd_text: str) -> float:
        """Calculate keyword similarity using TF-IDF cosine similarity."""
        try:
            # Ensure we have valid text
            if not resume_text or not jd_text:
                ats_logger.warning("Empty resume_text or jd_text in keyword similarity calculation")
                return 0.0
            
            # Minimum text length check
            resume_text = resume_text.strip()
            jd_text = jd_text.strip()
            
            if len(resume_text) < 10 or len(jd_text) < 10:
                ats_logger.warning(f"Insufficient text length - resume: {len(resume_text)}, jd: {len(jd_text)}")
                return 0.0
            
            # Log text samples for debugging
            ats_logger.info(f"Resume text sample (first 200 chars): {resume_text[:200]}")
            ats_logger.info(f"JD text sample (first 200 chars): {jd_text[:200]}")
            
            # Use more lenient TF-IDF settings to ensure we get matches
            vectorizer = TfidfVectorizer(
                max_features=200,  # Increased to capture more keywords
                stop_words='english',
                ngram_range=(1, 2),  # Unigrams and bigrams
                min_df=1,
                lowercase=True,
                token_pattern=r'\b[a-zA-Z][a-zA-Z]+\b'  # Match words with at least 2 letters
            )
            
            # Create TF-IDF vectors
            try:
                tfidf_matrix = vectorizer.fit_transform([resume_text, jd_text])
                
                # Check if we got valid vectors
                if tfidf_matrix.shape[0] < 2:
                    ats_logger.warning("TF-IDF matrix has insufficient rows")
                    return 0.0
                
                # Calculate cosine similarity
                similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
                
                # Convert to percentage
                tfidf_similarity_percent = similarity * 100
                
                # Log feature names for debugging
                feature_names = vectorizer.get_feature_names_out()
                ats_logger.info(f"TF-IDF features extracted: {len(feature_names)} features")
                ats_logger.info(f"TF-IDF cosine similarity: {tfidf_similarity_percent:.2f}% (raw: {similarity:.4f})")
                
                # ALWAYS calculate word overlap as a fallback/verification method
                resume_words = set(re.findall(WORD_REGEX, resume_text.lower())) - _STOP_WORDS
                jd_words = set(re.findall(WORD_REGEX, jd_text.lower())) - _STOP_WORDS

                overlap_percent = 0.0
                if jd_words:
                    overlap = len(resume_words & jd_words)
                    overlap_percent = (overlap / len(jd_words)) * 100
                    ats_logger.info(f"Word overlap: {overlap} common words out of {len(jd_words)} JD words = {overlap_percent:.2f}%")
                    ats_logger.info(f"Resume unique words: {len(resume_words)}, JD unique words: {len(jd_words)}")
                    if overlap > 0:
                        ats_logger.info(f"Sample overlapping words: {list(resume_words & jd_words)[:10]}")

                similarity_percent = _pick_final_similarity(tfidf_similarity_percent, overlap_percent)
                ats_logger.info(f"Combined similarity: TF-IDF={tfidf_similarity_percent:.2f}%, Overlap={overlap_percent:.2f}%, Final={similarity_percent:.2f}%")
                print(f"[ATS] Combined: TF-IDF={tfidf_similarity_percent:.2f}%, Overlap={overlap_percent:.2f}%, Final={similarity_percent:.2f}%")
                return similarity_percent
                
            except ValueError as ve:
                ats_logger.error(f"ValueError in TF-IDF calculation: {ve}")
                resume_words = set(re.findall(WORD_REGEX, resume_text.lower())) - _STOP_WORDS
                jd_words = set(re.findall(WORD_REGEX, jd_text.lower())) - _STOP_WORDS
                if jd_words:
                    overlap_percent = (len(resume_words & jd_words) / len(jd_words)) * 100
                    ats_logger.info(f"Using fallback word overlap: {overlap_percent:.2f}%")
                    return min(overlap_percent, 80.0)
                return 0.0
            
        except Exception as e:
            ats_logger.error(f"Error calculating keyword similarity: {e}", exc_info=True)
            return 0.0
    
    def _check_formatting_issues(self, pdf_path: str, resume_text: str) -> List[str]:
        """Check for ATS-unfriendly formatting issues."""
        issues = []
        
        # Check for tables (basic detection)
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    tables = page.extract_tables()
                    if tables:
                        issues.append("Tables detected - may not be parsed correctly by ATS")
                        break
        except Exception:
            pass

        # Check for images (if text is very short relative to PDF size)
        try:
            with pdfplumber.open(pdf_path) as pdf:
                total_chars = sum(len(page.extract_text() or "") for page in pdf.pages)
                if total_chars < 500 and len(pdf.pages) > 0:
                    issues.append("Possible image-based PDF - text may not be extractable")
        except Exception:
            pass
        
        # Check for special characters that might cause issues
        if re.search(r'[^\x00-\x7F]', resume_text):
            # Has non-ASCII characters - might be okay, but flag it
            pass
        
        # Check for missing summary section
        text_lower = resume_text.lower()
        if not re.search(r'\b(summary|objective|profile)\b', text_lower):
            issues.append("No summary/objective section found")
        
        return issues
    
    def _calculate_structure_score(self, sections: Dict[str, bool]) -> float:
        """
        Calculate structure score (30% of total).
        Points for having required sections.
        """
        score = 0.0
        max_score = 30.0
        
        # Required sections (10 points each)
        if sections.get("skills"):
            score += 10.0
        if sections.get("experience"):
            score += 10.0
        if sections.get("education"):
            score += 10.0
        
        return min(score, max_score)
    
    def _calculate_formatting_score(self, formatting_issues: List[str]) -> float:
        """
        Calculate formatting score (20% of total).
        Deduct points for formatting issues.
        """
        score = 20.0  # Start with full points

        # Deduct points for each issue
        penalty_per_issue = 5.0
        
        for issue in formatting_issues:
            if "table" in issue.lower():
                score -= penalty_per_issue
            elif "image" in issue.lower():
                score -= penalty_per_issue
            elif "summary" in issue.lower():
                score -= 3.0  # Smaller penalty for missing summary
        
        return max(score, 0.0)
    
    def _calculate_ats_score(
        self, 
        keyword_match_percent: float, 
        structure_score: float, 
        formatting_score: float
    ) -> float:
        """
        Calculate final ATS score (0-100).
        
        Formula:
        - Keyword Match: 50% (0-50 points)
        - Structure: 30% (0-30 points)
        - Formatting: 20% (0-20 points)
        """
        # Ensure inputs are valid numbers
        keyword_match_percent = float(keyword_match_percent) if keyword_match_percent is not None else 0.0
        structure_score = float(structure_score) if structure_score is not None else 0.0
        formatting_score = float(formatting_score) if formatting_score is not None else 0.0
        
        # Keyword match contributes 50% (scale 0-100% to 0-50 points)
        keyword_points = (keyword_match_percent / 100.0) * 50.0
        
        # Structure score is already 0-30
        structure_points = structure_score
        
        # Formatting score is already 0-20
        formatting_points = formatting_score
        
        total_score = keyword_points + structure_points + formatting_points
        
        # Log calculation breakdown
        ats_logger.info(f"Score breakdown - Keyword: {keyword_points:.2f} (from {keyword_match_percent:.1f}%), Structure: {structure_points:.2f}, Formatting: {formatting_points:.2f}, Total: {total_score:.2f}")
        
        # Normalize to 0-100
        final_score = min(max(total_score, 0.0), 100.0)
        
        return final_score
    
    def _find_missing_keywords(
        self, 
        jd_keywords: List[str], 
        resume_keywords: List[str]
    ) -> List[str]:
        """Find keywords in JD that are missing from resume."""
        jd_set = set(jd_keywords)
        resume_set = set(resume_keywords)
        
        missing = jd_set - resume_set
        
        # Filter out common words and return most relevant
        common_words = {
            "the", "and", "or", "but", "in", "on", "at", "to", "for",
            "of", "with", "by", "from", "as", "is", "are", "was", "were"
        }
        
        missing_filtered = [
            kw for kw in missing 
            if kw not in common_words and len(kw) > 3
        ]
        
        # Return sorted by length (longer keywords are usually more important)
        return sorted(missing_filtered, key=len, reverse=True)
    
    def _get_ai_suggestions(
        self,
        resume_text: str,
        job_description: str,
        missing_keywords: List[str],
        formatting_issues: List[str]
    ) -> List[str]:
        """
        Get AI-powered improvement suggestions using OpenAI.
        Only uses OpenAI for suggestions, NOT for scoring.
        """
        if not openai_client:
            return _fallback_ats_suggestions(
                missing_keywords, formatting_issues, "Review your resume for ATS compatibility"
            )

        try:
            prompt = f"""You are an ATS (Applicant Tracking System) expert. Analyze this resume against the job description and provide 3-5 specific, actionable improvement suggestions.

RESUME TEXT (first 2000 chars):
{resume_text[:2000]}

JOB DESCRIPTION (first 1500 chars):
{job_description[:1500]}

MISSING KEYWORDS: {', '.join(missing_keywords[:10])}

FORMATTING ISSUES: {', '.join(formatting_issues) if formatting_issues else 'None detected'}

Provide 3-5 concise, actionable suggestions (one per line) to improve ATS compatibility. Focus on:
1. Adding missing keywords naturally
2. Fixing formatting issues
3. Improving structure
4. General ATS best practices

Format as a simple list, one suggestion per line, no numbering."""

            response = openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an ATS expert providing resume improvement suggestions."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.7
            )

            suggestions_text = response.choices[0].message.content.strip()
            suggestions = [s.strip() for s in suggestions_text.split('\n') if s.strip()]
            return suggestions[:5]

        except Exception as e:
            ats_logger.error(f"Error getting AI suggestions: {e}")
            return _fallback_ats_suggestions(
                missing_keywords,
                formatting_issues,
                "Review your resume for better ATS compatibility",
                keyword_prefix="Add these keywords naturally:",
                include_formatting_detail=False
            )
    
    def _build_resume_text_from_data(self, resume_data: Dict) -> str:
        """Build resume text from structured data."""
        step1 = resume_data.get("step1", {}) or {}
        text_parts = []
        text_parts.extend(_step1_parts(step1))
        text_parts.extend(_step4_skills_parts(resume_data.get("step4", [])))
        text_parts.extend(_step2_education_parts(resume_data.get("step2", {}) or {}))
        text_parts.extend(_step3_experience_parts(resume_data.get("step3", [])))
        text_parts.extend(_step1_languages_parts(step1))
        text_parts.extend(_step1_certs_parts(step1))
        text_parts.extend(_custom_sections_parts(resume_data.get("customSections", [])))

        resume_text = " ".join(text_parts)
        ats_logger.info(f"Built resume text length: {len(resume_text)} characters")
        ats_logger.info(f"Resume text preview: {resume_text[:300]}...")
        return resume_text
    
    def _detect_sections_from_data(self, resume_data: Dict) -> Dict[str, bool]:
        """Detect resume sections from structured data."""
        sections = {
            "summary": False,
            "skills": False,
            "experience": False,
            "education": False,
            "projects": False,
            "certifications": False,
            "languages": False
        }
        
        step1 = resume_data.get("step1", {})
        step2 = resume_data.get("step2", {})
        step3 = resume_data.get("step3", [])
        step4 = resume_data.get("step4", [])
        
        sections["summary"] = bool(step1.get("summary"))
        sections["skills"] = bool(step4 and len(step4) > 0)
        sections["experience"] = bool(step3 and len(step3) > 0)
        sections["education"] = bool(step2 and (step2.get("degree") or step2.get("institution") or step2.get("school")))
        sections["languages"] = bool(step1.get("languages"))
        sections["certifications"] = bool(step1.get("certificates") or step1.get("certs"))
        
        # Check for projects in custom sections or experience descriptions
        custom_sections = resume_data.get("customSections", [])
        for section in custom_sections:
            if section.get("name", "").lower() in ["projects", "project"]:
                sections["projects"] = True
                break
        
        # Also check experience descriptions for project-like content
        if step3:
            for exp in step3:
                desc = exp.get("description", "").lower()
                if "project" in desc or len(desc) > 200:  # Long descriptions might indicate projects
                    sections["projects"] = True
                    break
        
        return sections
