from repo.resume_repo import ResumeRepo
from repo.user_repo import UserRepo
from ai.resume_generator import generate_ai_resume
from datetime import datetime, timezone
from utils.crypto_utils import CryptoUtils

resume_repo = ResumeRepo()
user_repo = UserRepo()


def _to_list(val):
    """Normalize languages/certificates to list of strings."""
    if not val:
        return []
    if isinstance(val, list):
        return [str(x).strip() for x in val if x]
    if isinstance(val, str):
        return [x.strip() for x in val.split("\n") if x.strip()]
    return []


def _merge_skills(user_skills, ai_skills):
    """User form skills first, then AI suggestions not already present. All strings."""
    seen = set()
    out = []
    for s in user_skills:
        if s and s not in seen:
            seen.add(s)
            out.append(s)
    for s in (ai_skills or []):
        ss = (s.get("name") if isinstance(s, dict) else s) or ""
        if isinstance(ss, str):
            ss = ss.strip()
        if ss and ss not in seen:
            seen.add(ss)
            out.append(ss)
    return out


def create_ai_resume(user_email, payload):
    print("CREATE AI RESUME PAYLOAD:", payload)
    role = payload.get("role")
    jd = payload.get("job_description")
    exp_level = payload.get("experience_level")

    personal = payload.get("personal", {}) or {}
    education = payload.get("education", {}) or {}
    experience = payload.get("experience", []) or []
    skills_raw = payload.get("skills", [])
    # Normalize skills: frontend may send array of strings or single string
    if isinstance(skills_raw, str):
        skills = [s.strip() for s in skills_raw.split("\n") if s.strip()]
    else:
        skills = [s.strip() for s in skills_raw if isinstance(s, str) and s.strip()]

    ai_context = {
        "role": role,
        "job_description": jd,
        "experience_level": exp_level,
        "personal": personal,
        "education": education,
        "experience": experience,
        "skills": skills if skills else None
    }

    print("AI CONTEXT:", ai_context)

    ai_output = generate_ai_resume(ai_context)
    print("AI OUTPUT:", ai_output)
    # ---------------- BUILD STEP-BASED DATA ----------------

    resume_data = {
        "step1": {
            "name": (personal.get("name") or "").strip(),
            "title": (personal.get("title") or "").strip(),
            "email": (personal.get("email") or "").strip(),
            "phone": (personal.get("phone") or "").strip(),
            "location": (personal.get("location") or "").strip(),
            "summary": (ai_output.get("summary") or personal.get("summary") or "").strip(),
            "languages": _to_list(personal.get("languages")),
            "certificates": _to_list(personal.get("certificates"))
        },

        "step2": {
            "institution": (education.get("institution") or "").strip(),
            "degree": (education.get("degree") or "").strip(),
            "field": (education.get("field") or "").strip(),
            "year": (education.get("year") or "").strip()
        },

        "step3": experience,

        # SKILLS: user form skills first, then AI-only skills so all entered data shows
        "step4": _merge_skills(skills, ai_output.get("skills") or [])
    }

    from services.resume_score_service import calculate_resume_score

    temp_resume = {"data": resume_data}
    score, _, _ = calculate_resume_score(temp_resume)

    # encoded_email = user_repo.encode_email(user_email)
    encoded_email = CryptoUtils.encode(user_email)
    
    # Get template from payload, default to "professionalBlue" if not provided
    template = payload.get("template", "professionalBlue")
    
    resume = {
        "user_email": encoded_email,
        "title": f"AI Resume - {role}",
        "template": template,
        "data": resume_data,
        "created_at": datetime.now(timezone.utc)
    }

    result = resume_repo.create(resume)
    return str(result.inserted_id)
