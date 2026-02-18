"""
ATS Resume Score Checker Controller
Handles PDF upload and job description analysis requests.
"""

from flask import Blueprint, request, jsonify, session
from werkzeug.utils import secure_filename
from services.ats_checker_service import ATSCheckerService
from services.resume_service import ResumeService
from services.resume_score_service import calculate_resume_score
from utils.logger import setup_logger
from bson import ObjectId

ats_controller_logger = setup_logger(
    name="ATS_CONTROLLER",
    log_file="ats_controller.log"
)

ats_bp = Blueprint("ats", __name__, url_prefix="/api/ats")
ats_service = ATSCheckerService()
resume_service = ResumeService()

# Allowed file extensions
ALLOWED_EXTENSIONS = {'pdf'}


def allowed_file(filename: str) -> bool:
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@ats_bp.route("/check", methods=["POST"])
def check_resume():
    """
    ATS Resume Score Checker endpoint.
    
    Accepts:
    - resume: PDF file (multipart/form-data)
    - job_description: string (multipart/form-data or JSON)
    
    Returns:
    - JSON response with ATS score and analysis
    """
    try:
        # Check if resume file is present
        if 'resume' not in request.files:
            return jsonify({
                "error": "No resume file provided",
                "ats_score": 0
            }), 400
        
        resume_file = request.files['resume']
        
        # Validate file
        if resume_file.filename == '':
            return jsonify({
                "error": "No file selected",
                "ats_score": 0
            }), 400
        
        if not allowed_file(resume_file.filename):
            return jsonify({
                "error": "Invalid file type. Only PDF files are allowed.",
                "ats_score": 0
            }), 400
        
        # Get job description
        job_description = None
        
        # Try to get from form data first
        if 'job_description' in request.form:
            job_description = request.form['job_description']
        # Try JSON body as fallback
        elif request.is_json and 'job_description' in request.json:
            job_description = request.json['job_description']
        
        if not job_description or not job_description.strip():
            return jsonify({
                "error": "Job description is required",
                "ats_score": 0
            }), 400
        
        # Process resume check
        result = ats_service.check_resume(resume_file, job_description.strip())
        
        # Check if there was an error in processing
        if "error" in result:
            return jsonify(result), 400
        
        return jsonify(result), 200
        
    except Exception as e:
        ats_controller_logger.error(f"Error in check_resume endpoint: {str(e)}", exc_info=True)
        return jsonify({
            "error": f"Internal server error: {str(e)}",
            "ats_score": 0
        }), 500


@ats_bp.route("/check-from-resume", methods=["POST"])
def check_resume_from_saved():
    """
    ATS Resume Score Checker endpoint using saved resume data.
    This bypasses PDF parsing and uses the structured resume data directly.
    
    Accepts:
    - resume_id: string (JSON body)
    - job_description: string (JSON body)
    
    Returns:
    - JSON response with ATS score and analysis
    """
    try:
        # Check authentication
        if "user" not in session:
            return jsonify({
                "error": "Authentication required",
                "ats_score": 0
            }), 401
        
        # Get request data
        data = request.get_json()
        
        if not data:
            return jsonify({
                "error": "Request body is required",
                "ats_score": 0
            }), 400
        
        resume_id = data.get("resume_id")
        job_description = data.get("job_description")
        
        # Validate inputs
        if not resume_id:
            return jsonify({
                "error": "resume_id is required",
                "ats_score": 0
            }), 400
        
        if not job_description or not job_description.strip():
            return jsonify({
                "error": "job_description is required",
                "ats_score": 0
            }), 400
        
        # Get resume data
        resume = resume_service.get_resume_by_id(resume_id)
        
        if not resume:
            return jsonify({
                "error": "Resume not found",
                "ats_score": 0
            }), 404
        
        # Verify ownership
        user_email = session["user"]["email"]
        from utils.crypto_utils import CryptoUtils
        encoded_email = CryptoUtils.encode(user_email)
        if resume.get("user_email") != encoded_email:
            return jsonify({
                "error": "Unauthorized access to resume",
                "ats_score": 0
            }), 403
        
        # Get resume data
        resume_data = resume.get("data", {})
        
        if not resume_data:
            return jsonify({
                "error": "Resume data is empty",
                "ats_score": 0
            }), 400
        
        # Process ATS check using resume data
        result = ats_service.check_resume_from_data(resume_data, job_description.strip())
        
        # Use same score as card/preview (resume_score) so ATS checker matches everywhere
        resume_score, breakdown, warnings = calculate_resume_score(resume)
        result["resume_score"] = resume_score
        result["ats_score"] = resume_score  # Unify: display same score as cards and preview
        
        # Log the result before returning
        ats_controller_logger.info(f"ATS check result: ats_score={result.get('ats_score')}, resume_score={resume_score}, keyword_match={result.get('keyword_match_percent')}")
        
        # Check if there was an error in processing
        if "error" in result:
            return jsonify(result), 400
        
        # Ensure ats_score is present and valid
        if "ats_score" not in result or result["ats_score"] is None:
            ats_controller_logger.error("ATS score missing from result, setting to 0")
            result["ats_score"] = 0
        
        return jsonify(result), 200
        
    except Exception as e:
        ats_controller_logger.error(f"Error in check_resume_from_saved endpoint: {str(e)}", exc_info=True)
        return jsonify({
            "error": f"Internal server error: {str(e)}",
            "ats_score": 0
        }), 500
