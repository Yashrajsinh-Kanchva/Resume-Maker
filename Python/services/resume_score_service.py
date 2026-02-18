"""
Resume score calculation with validation and granular scoring.
Returns score 0-100 (e.g. 51, 52), breakdown by category, and data-quality warnings.
"""
import re


def _looks_like_garbage(s, field_name="field"):
    """Return True if string looks like placeholder/garbage (numbers only, repeated chars, etc.)."""
    if not s or not isinstance(s, str):
        return False
    s = s.strip()
    if len(s) < 2:
        return True
    # Mostly digits (e.g. 11111, 12345)
    digit_ratio = sum(c.isdigit() for c in s) / len(s)
    if digit_ratio >= 0.7:
        return True
    # Same character repeated (aaa, 111, xxx)
    if len(set(s.lower())) <= 1:
        return True
    # Only digits
    if s.isdigit():
        return True
    # Very short "name" that looks like abbrev or test
    if field_name == "name" and len(s) < 3 and not s.isalpha():
        return True
    # No letters at all
    if not any(c.isalpha() for c in s):
        return True
    return False


def _name_warning(step1):
    """Return warning string for name field, or None if ok."""
    name = (step1.get("name") or "").strip() if step1 else ""
    if not name:
        return "Name is missing."
    if _looks_like_garbage(name, "name"):
        return "Name looks invalid (e.g. numbers or placeholder). Use your real name."
    return None


def _validate_step1(step1):
    """Validate step1 (profile) fields. Returns list of warning strings."""
    warnings = []
    if not step1:
        return warnings
    w = _name_warning(step1)
    if w:
        warnings.append(w)
    title = (step1.get("title") or "").strip()
    if title and _looks_like_garbage(title, "title"):
        warnings.append("Job title looks invalid. Enter a proper job title.")
    email = (step1.get("email") or "").strip()
    if email and ("@" not in email or len(email) < 5):
        warnings.append("Email format may be wrong.")
    elif not email:
        warnings.append("Email is missing.")
    summary = (step1.get("summary") or "").strip()
    if summary and _looks_like_garbage(summary, "summary"):
        warnings.append("Summary looks like placeholder text. Write a short professional summary.")
    return warnings


def _validate_step2(step2):
    """Validate step2 (education). Returns list of warning strings."""
    if not step2:
        return []
    degree = (step2.get("degree") or "").strip()
    if degree and _looks_like_garbage(degree, "degree"):
        return ["Degree/education may be invalid. Check education details."]
    return []


def _validate_step3_experience(step3):
    """Validate step3 (experience) entries. Returns list of warning strings."""
    warnings = []
    if not step3 or not isinstance(step3, list):
        return warnings
    for i, exp in enumerate(step3):
        if not isinstance(exp, dict):
            continue
        job_title = (exp.get("jobTitle") or exp.get("job_title") or "").strip()
        if job_title and _looks_like_garbage(job_title, "job"):
            warnings.append(f"Experience #{i+1} job title looks invalid.")
        employer = (exp.get("employer") or exp.get("company") or "").strip()
        if employer and _looks_like_garbage(employer, "employer"):
            warnings.append(f"Experience #{i+1} employer name may be wrong.")
    return warnings


def _validate_resume_data(data):
    """Check for invalid/placeholder values. Returns list of warning strings."""
    warnings = []
    warnings.extend(_validate_step1(data.get("step1", {})))
    warnings.extend(_validate_step2(data.get("step2", {})))
    warnings.extend(_validate_step3_experience(data.get("step3", [])))
    return warnings


def _skill_text(s):
    if isinstance(s, str):
        return s.strip()
    if isinstance(s, dict):
        v = s.get("name") or s.get("skill") or s.get("title") or ""
        return str(v).strip() if v is not None else ""
    return ""


def _profile_score(step1):
    """Profile (name, title, summary) 0-15."""
    name_ok = bool((step1.get("name") or "").strip()) and not _looks_like_garbage((step1.get("name") or "").strip(), "name")
    title_ok = bool((step1.get("title") or "").strip()) and not _looks_like_garbage((step1.get("title") or "").strip(), "title")
    summary_filled = bool((step1.get("summary") or "").strip())
    return min((5.0 if name_ok else 0) + (4.0 if title_ok else 0) + (6.0 if summary_filled else 0), 15.0)


def _summary_quality_score(step1):
    """Summary quality 0-15 by length and garbage check."""
    summary = (step1.get("summary") or "").strip()
    if _looks_like_garbage(summary, "summary") or not summary:
        return 0.0
    n = len(summary)
    if n >= 100:
        return 15.0
    if n >= 80:
        return 13.0
    if n >= 60:
        return 11.0
    if n >= 40:
        return 8.0
    if n >= 20:
        return 5.0
    return 2.5


def _skills_score(step4):
    """Skills 0-20."""
    num_skills = sum(1 for s in step4 if _skill_text(s))
    return min(num_skills * 3.2, 20.0)


def _experience_score(step3):
    """Experience 0-20."""
    num_exp = len([e for e in step3 if isinstance(e, dict) and (e.get("jobTitle") or e.get("job_title") or "").strip()])
    desc_lengths = [len((e.get("description") or "").strip()) for e in step3 if isinstance(e, dict)]
    if num_exp >= 2:
        long_desc_count = sum(1 for d in desc_lengths if d > 80)
        return min(15.0 + min(long_desc_count * 2.5, 5.0), 20.0)
    if num_exp == 1:
        d = desc_lengths[0] if desc_lengths else 0
        if d < 50:
            return 7.0
        if d < 120:
            return 10.0
        return 13.0
    return 0.0


def _education_score(step2):
    """Education 0-10."""
    if not step2:
        return 0.0
    degree = (step2.get("degree") or "").strip()
    has_degree = bool(degree) and not _looks_like_garbage(degree, "degree")
    has_institution = bool((step2.get("institution") or step2.get("school") or "").strip())
    return min((5.0 if has_degree else 0.0) + (5.0 if has_institution else 0.0), 10.0)


def _projects_score(step3):
    """Projects / content depth 0-10."""
    desc_lengths = [len((e.get("description") or "").strip()) for e in step3 if isinstance(e, dict)]
    project_like = sum(1 for d in desc_lengths if d > 50)
    if project_like >= 3:
        return 10.0
    if project_like == 2:
        return 7.0
    if project_like == 1:
        return 4.0
    return 0.0


def _ats_keywords_score(step1, step3):
    """ATS keywords 0-10."""
    summary = (step1.get("summary") or "").strip()
    descs = " ".join(str(e.get("description") or "") for e in step3 if isinstance(e, dict))
    text = (summary + " " + descs).lower()
    keywords = ["python", "java", "javascript", "sql", "api", "react", "node", "aws", "docker", "git", "agile", "leadership", "communication", "analysis", "development", "design", "management"]
    matches = sum(1 for k in keywords if k in text)
    return min(matches * 2.2, 10.0)


def calculate_resume_score(resume):
    """
    Calculate resume score 0-100 with granular breakdown.
    Returns (score, breakdown, warnings).
    """
    data = resume.get("data", {}) or {}
    step1 = data.get("step1", {}) or {}
    step2 = data.get("step2", {}) or {}
    step3 = data.get("step3", []) or []
    step4 = data.get("step4", []) or []

    warnings = _validate_resume_data(data)

    breakdown = {
        "Profile": round(_profile_score(step1), 1),
        "Summary": round(_summary_quality_score(step1), 1),
        "Skills": round(_skills_score(step4), 1),
        "Experience": round(_experience_score(step3), 1),
        "Education": round(_education_score(step2), 1),
        "Projects": round(_projects_score(step3), 1),
        "ATS": round(_ats_keywords_score(step1, step3), 1),
    }
    total = sum(breakdown.values())
    final_score = min(max(0, int(round(total))), 100)
    return final_score, breakdown, warnings
