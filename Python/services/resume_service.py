from datetime import datetime
from repo.resume_repo import ResumeRepo
from utils.crypto_utils import CryptoUtils
from bson import ObjectId
from utils.logger import setup_logger

service_logger = setup_logger(
    name="RESUME_SERVICE",
    log_file="service.log"
)

class ResumeService:
    def __init__(self):
        self.repo = ResumeRepo()

    # ✅ ADMIN: GET ALL RESUMES (FOR LIST + CSV)
    def get_all_resumes_for_admin(self):
        resumes = self.repo.find_all_resumes()
        result = []

        for r in resumes:
            result.append({
                "email": CryptoUtils.decode(r.get("user_email", "")),
                "title": r.get("title", ""),
                "created_at": r.get("created_at")
            })

        return result

    # ---------------- USER ACTIONS ----------------
    def create_resume(self, email, payload):
        if not payload or "data" not in payload:
            return {"success": False, "message": "Invalid resume data"}

        # Auto-generate title if not provided or if it's a generic name
        title = payload.get("title", "").strip()
        template = payload.get("template", "")
        
        if not title or title.lower() in ["untitled resume", "my resume", "resume"]:
            # Generate descriptive title with template and date
            template_names = {
                "academicYellow": "Academic Yellow",
                "professionalBlue": "Professional Blue",
                "minimalElegant": "Minimal Elegant",
                "blueCorporate": "Blue Corporate",
                "softGreenMinimal": "Soft Green",
                "darkElegant": "Dark Elegant",
                "timelineResume": "Timeline",
                "boldRedAccent": "Bold Red",
                "cardBased": "Card Based",
                "glassmorphism": "Glassmorphism",
                "infographic": "Infographic",
                "ultraMinimal": "Ultra Minimal",
                "boxShadow": "Box Shadow",
                "classicSerif": "Classic Serif",
                "freshGradient": "Fresh Gradient",
                "splitHeaderModern": "Split Header",
                "techLook": "Tech Look",
                "ultraClean": "Ultra Clean"
            }
            
            template_display = template_names.get(template, template or "Resume")
            now = datetime.utcnow()
            date_str = now.strftime("%b %d, %Y")
            time_str = now.strftime("%I:%M %p")
            title = f"{template_display} - {date_str} {time_str}"

        resume = {
            "user_email": CryptoUtils.encode(email),
            "title": title,
            "template": template,
            "data": payload["data"],
            "created_at": datetime.utcnow()
        }

        self.repo.create(resume)
        return {"success": True, "message": "Resume saved"}

    def get_user_resumes(self, email):
        encoded_email = CryptoUtils.encode(email)
        resumes = self.repo.find_by_user(encoded_email)

        for r in resumes:
            r["_id"] = str(r["_id"])

        return resumes

    def get_resume_by_id(self, resume_id):
        """
        Get resume by ID with ObjectId validation.
        
        Args:
            resume_id: String ID to validate and convert to ObjectId
            
        Returns:
            Resume dict if found, None otherwise (including invalid ID format)
        """
        # Validate ObjectId format before attempting conversion
        # This prevents bson.errors.InvalidId exceptions from being raised
        if not resume_id or not isinstance(resume_id, str):
            return None
        
        # Check if the string is a valid ObjectId format (24 hex characters)
        if not ObjectId.is_valid(resume_id):
            service_logger.warning(f"Invalid ObjectId format received: {resume_id[:50]}")
            return None
        
        try:
            resume = self.repo.find_by_id(ObjectId(resume_id))
            if not resume:
                return None

            resume["_id"] = str(resume["_id"])
            return resume
        except Exception as e:
            # Catch any unexpected errors during conversion or lookup
            service_logger.error(f"Error retrieving resume by ID: {str(e)}", exc_info=True)
            return None

    def delete_resume(self, email, resume_id):
        encoded_email = CryptoUtils.encode(email)
        return self.repo.delete_by_id(encoded_email, resume_id)
