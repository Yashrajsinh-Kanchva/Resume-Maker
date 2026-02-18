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


def _validate_resume_data(data):
    """Check for invalid/placeholder values. Returns list of warning strings."""
    warnings = []
    step1 = data.get("step1", {})

    name = (step1.get("name") or "").strip()
    if name and _looks_like_garbage(name, "name"):
        warnings.append("Name looks invalid (e.g. numbers or placeholder). Use your real name.")
    elif not name:
        warnings.append("Name is missing.")

    title = (step1.get("title") or "").strip()
    if title and _looks_like_garbage(title, "title"):
        warnings.append("Job title looks invalid. Enter a proper job title.")

    email = (step1.get("email") or "").strip()
    if email:
        # Basic email check: has @ and something after
        if "@" not in email or len(email) < 5:
            warnings.append("Email format may be wrong.")
    else:
        warnings.append("Email is missing.")

    summary = (step1.get("summary") or "").strip()
    if summary and _looks_like_garbage(summary, "summary"):
        warnings.append("Summary looks like placeholder text. Write a short professional summary.")

    step2 = data.get("step2", {})
    degree = (step2.get("degree") or "").strip() if step2 else ""
    if degree and _looks_like_garbage(degree, "degree"):
        warnings.append("Degree/education may be invalid. Check education details.")

    step3 = data.get("step3", [])
    if isinstance(step3, list):
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


def calculate_resume_score(resume):
    """
    Calculate resume score 0-100 with granular breakdown.
    Returns (score, breakdown, warnings).
    - score: int 0-100 (e.g. 51, 52) for display
    - breakdown: dict of category -> points (can be float for granularity)
    - warnings: list of strings (data quality / validation issues)
    """
    data = resume.get("data", {})
    step1 = data.get("step1", {})
    step2 = data.get("step2", {})
    step3 = data.get("step3", []) or []
    step4 = data.get("step4", []) or []

    warnings = _validate_resume_data(data)

    # Use floats for granular scoring so total can be 51.3 -> 51, 52.7 -> 53
    total = 0.0
    breakdown = {}

    # ---------- PROFILE (0-15) ----------
    name_ok = bool((step1.get("name") or "").strip()) and not _looks_like_garbage((step1.get("name") or "").strip(), "name")
    title_ok = bool((step1.get("title") or "").strip()) and not _looks_like_garbage((step1.get("title") or "").strip(), "title")
    summary_filled = bool((step1.get("summary") or "").strip())
    profile_score = 0.0
    if name_ok:
        profile_score += 5.0
    if title_ok:
        profile_score += 4.0
    if summary_filled:
        profile_score += 6.0
    breakdown["Profile"] = round(min(profile_score, 15.0), 1)
    total += breakdown["Profile"]

    # ---------- SUMMARY QUALITY (0-15) ----------
    summary = (step1.get("summary") or "").strip()
    if _looks_like_garbage(summary, "summary"):
        summary_score = 0.0
    elif len(summary) >= 100:
        summary_score = 15.0
    elif len(summary) >= 80:
        summary_score = 13.0
    elif len(summary) >= 60:
        summary_score = 11.0
    elif len(summary) >= 40:
        summary_score = 8.0
    elif len(summary) >= 20:
        summary_score = 5.0
    elif len(summary) > 0:
        summary_score = 2.5
    else:
        summary_score = 0.0
    breakdown["Summary"] = round(summary_score, 1)
    total += breakdown["Summary"]

    # ---------- SKILLS (0-20) ----------
    def _skill_text(s):
        if isinstance(s, str):
            return s.strip()
        if isinstance(s, dict):
            v = s.get("name") or s.get("skill") or s.get("title") or ""
            return str(v).strip() if v is not None else ""
        return ""

    num_skills = sum(1 for s in step4 if _skill_text(s))
    skills_score = min(num_skills * 3.2, 20.0)  # 3.2 per skill -> 6.4, 9.6, ... 19.2, 20
    breakdown["Skills"] = round(skills_score, 1)
    total += breakdown["Skills"]

    # ---------- EXPERIENCE (0-20) ----------
    num_exp = len([e for e in step3 if isinstance(e, dict) and (e.get("jobTitle") or e.get("job_title") or "").strip()])
    desc_lengths = [len((e.get("description") or "").strip()) for e in step3 if isinstance(e, dict)]
    if num_exp >= 2:
        # Quality: long descriptions get extra
        long_desc_count = sum(1 for d in desc_lengths if d > 80)
        exp_score = 15.0 + min(long_desc_count * 2.5, 5.0)  # 15-20
    elif num_exp == 1:
        d = desc_lengths[0] if desc_lengths else 0
        exp_score = 7.0 if d < 50 else 10.0 if d < 120 else 13.0
    else:
        exp_score = 0.0
    breakdown["Experience"] = round(min(exp_score, 20.0), 1)
    total += breakdown["Experience"]

    # ---------- EDUCATION (0-10) ----------
    has_degree = bool((step2.get("degree") or "").strip()) and not _looks_like_garbage((step2.get("degree") or "").strip(), "degree")
    has_institution = bool((step2.get("institution") or step2.get("school") or "").strip())
    edu_score = (5.0 if has_degree else 0.0) + (5.0 if has_institution else 0.0)
    breakdown["Education"] = round(min(edu_score, 10.0), 1)
    total += breakdown["Education"]

    # ---------- PROJECTS / CONTENT DEPTH (0-10) ----------
    project_like = sum(1 for d in desc_lengths if d > 50)
    if project_like >= 3:
        proj_score = 10.0
    elif project_like == 2:
        proj_score = 7.0
    elif project_like == 1:
        proj_score = 4.0
    else:
        proj_score = 0.0
    breakdown["Projects"] = round(proj_score, 1)
    total += breakdown["Projects"]

    # ---------- ATS KEYWORDS (0-10) ----------
    keywords = ["python", "java", "javascript", "sql", "api", "react", "node", "aws", "docker", "git", "agile", "leadership", "communication", "analysis", "development", "design", "management"]
    text = (summary + " " + " ".join(str(e.get("description") or "") for e in step3 if isinstance(e, dict))).lower()
    matches = sum(1 for k in keywords if k in text)
    ats_score = min(matches * 2.2, 10.0)  # 2.2 per match -> 2.2, 4.4, 6.6, 8.8, 10
    breakdown["ATS"] = round(ats_score, 1)
    total += breakdown["ATS"]

    # Final total: round to int for display (51, 52, 53...)
    final_score = min(max(0, int(round(total))), 100)
    return final_score, breakdown, warnings
