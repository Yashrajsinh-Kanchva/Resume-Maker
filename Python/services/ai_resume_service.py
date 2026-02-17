from repo.resume_repo import ResumeRepo
from repo.user_repo import UserRepo
from ai.resume_generator import generate_ai_resume
from datetime import datetime, timezone
from utils.crypto_utils import CryptoUtils

resume_repo = ResumeRepo()
user_repo = UserRepo()

def create_ai_resume(user_email, payload):
    print("CREATE AI RESUME PAYLOAD:", payload)
    role = payload.get("role")
    jd = payload.get("job_description")
    exp_level = payload.get("experience_level")

    personal = payload.get("personal", {})
    education = payload.get("education", {})
    experience = payload.get("experience", [])
    skills = payload.get("skills", [])

    ai_context = {
        "role": role,
        "job_description": jd,
        "experience_level": exp_level,
        "personal": personal,
        "education": education,
        "experience": experience,
        "skills": skills
    }

    print("AI CONTEXT:", ai_context)

    ai_output = generate_ai_resume(ai_context)
    print("AI OUTPUT:", ai_output)
    # ---------------- BUILD STEP-BASED DATA ----------------

    resume_data = {
        "step1": {
            "name": personal.get("name", ""),
            "title": personal.get("title", ""),
            "email": personal.get("email", ""),
            "phone": personal.get("phone", ""),
            "location": personal.get("location", ""),
            "summary": ai_output.get("summary") or personal.get("summary", ""),
            "languages": personal.get("languages", []),
            "certificates": personal.get("certificates", [])
        },

        "step2": {
          "institution": education.get("institution", ""),
          "degree": education.get("degree", ""),
          "field": education.get("field", ""),
          "year": education.get("year", "")
        },


        # EXPERIENCE
        "step3": experience,

        # SKILLS
        "step4": ai_output.get("skills", [])
    }

    from services.resume_score_service import calculate_resume_score

    temp_resume = {"data": resume_data}
    score, _ = calculate_resume_score(temp_resume)

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
