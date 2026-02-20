# ATS Resume Score Checker - Setup Guide

## Installation Steps

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Download spaCy English Model

The ATS checker uses spaCy for NLP processing. You need to download the English model:

```bash
python -m spacy download en_core_web_sm
```

**Note:** This is a one-time setup. The model will be downloaded and cached locally.

### 3. Set OpenAI API Key (Optional)

The ATS checker works without OpenAI, but AI-powered suggestions require an API key:

1. Get your API key from https://platform.openai.com/api-keys
2. Add to your `.env` file:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

**Note:** Without OpenAI API key, the system will provide basic fallback suggestions.

### 4. Verify Installation

Start your Flask server and test the endpoint:

```bash
# Test endpoint
curl -X POST http://localhost:5000/api/ats/check \
  -F "resume=@your_resume.pdf" \
  -F "job_description=Your job description text here"
```

## Features

- ✅ PDF text extraction using pdfplumber
- ✅ Section detection (Summary, Skills, Experience, Education, etc.)
- ✅ Keyword matching using TF-IDF + cosine similarity
- ✅ ATS score calculation (0-100)
- ✅ Missing keywords identification
- ✅ Formatting issue detection
- ✅ AI-powered improvement suggestions (with OpenAI)

## API Endpoint

**POST** `/api/ats/check`

**Request:**
- `resume`: PDF file (multipart/form-data)
- `job_description`: string (multipart/form-data)

**Response:**
```json
{
  "ats_score": 78.5,
  "keyword_match_percent": 72.3,
  "missing_keywords": ["Docker", "Kubernetes"],
  "sections_found": {
    "skills": true,
    "experience": true,
    "education": true,
    "summary": false
  },
  "formatting_issues": [
    "Tables detected - may not be parsed correctly by ATS"
  ],
  "ai_suggestions": [
    "Add missing keywords naturally in experience section",
    "Avoid tables for ATS compatibility"
  ],
  "structure_score": 30.0,
  "formatting_score": 15.0
}
```

## Troubleshooting

### spaCy Model Not Found
If you see: `spaCy model 'en_core_web_sm' not found`
- Run: `python -m spacy download en_core_web_sm`

### PDF Extraction Fails
- Ensure PDF contains readable text (not just images)
- Try converting scanned PDFs to text first

### OpenAI Errors
- Check your API key is set correctly
- Verify you have API credits available
- System will work with fallback suggestions if OpenAI fails
