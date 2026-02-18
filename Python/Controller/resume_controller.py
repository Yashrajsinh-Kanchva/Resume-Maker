"""
Resume API controller.

Handles CRUD and related operations for user resumes: create, list, get by id,
score, skill frequency, navigation state, and delete. All resume-id routes
validate ID format before calling the service to avoid passing user-controlled
data unsanitized.
"""

from typing import Any, Optional, Tuple

from bson import ObjectId
from flask import Blueprint, Response, jsonify, request, session

from services.navigation_stack_service import go_back, open_view
from services.resume_ranking_service import rank_resumes
from services.resume_score_service import calculate_resume_score
from services.resume_service import ResumeService
from services.skill_frequency_service import get_skill_frequency
from utils.logger import setup_logger

resume_bp = Blueprint("resume", __name__)
resume_service = ResumeService()
resume_logger = setup_logger(name="RESUME_CONTROLLER", log_file="resume_controller.log")

ERROR_RESUME_NOT_FOUND = "Resume not found"
MSG_RESUME_NOT_FOUND_OR_NOT_ALLOWED = "Resume not found or not allowed"


def _get_user_email() -> Optional[str]:
    """Return the current user's email from session, or None if not authenticated."""
    if not session or "user" not in session:
        return None
    return session.get("user", {}).get("email")


def _is_valid_resume_id(resume_id: Any) -> bool:
    """
    Return True if resume_id is a non-empty string with valid MongoDB ObjectId format.

    Used to validate path/query parameters before passing to the service layer.
    """
    if not resume_id or not isinstance(resume_id, str):
        return False
    return bool(resume_id.strip()) and ObjectId.is_valid(resume_id)


@resume_bp.post("/")
def create_resume() -> Tuple[Response, int] | Response:
    """
    Create a new resume for the authenticated user.

    Expects JSON body with resume data. Returns 401 if not authenticated.
    """
    email = _get_user_email()
    if not email:
        return jsonify({"success": False, "message": "Unauthorized"}), 401

    data = request.get_json()
    result = resume_service.create_resume(email, data)

    if result.get("success"):
        resume_logger.info("Resume created successfully")
    else:
        resume_logger.info("Resume create rejected: %s", result.get("message", "unknown"))

    return jsonify(result)


@resume_bp.get("/")
def get_resumes() -> Tuple[Response, int] | Response:
    """
    Return the list of resumes for the authenticated user, with ranking applied.

    Returns 401 if not authenticated.
    """
    email = _get_user_email()
    if not email:
        return jsonify([]), 401

    resumes = resume_service.get_user_resumes(email)
    ranked_resumes = rank_resumes(resumes)
    open_view("documents")
    return jsonify(ranked_resumes)


@resume_bp.get("/<resume_id>")
def get_single_resume(resume_id: str) -> Tuple[Response, int] | Response:
    """
    Return a single resume by id for the authenticated user.

    Returns 401 if not authenticated, 404 if resume id is invalid or not found.
    """
    if not _get_user_email():
        return jsonify({"success": False}), 401

    if not _is_valid_resume_id(resume_id):
        return jsonify({"error": ERROR_RESUME_NOT_FOUND}), 404

    resume = resume_service.get_resume_by_id(resume_id)
    if not resume:
        return jsonify({"error": ERROR_RESUME_NOT_FOUND}), 404

    return jsonify(resume)


@resume_bp.get("/score/<resume_id>")
def get_resume_score(resume_id: str) -> Tuple[Response, int] | Response:
    """
    Return ATS score, breakdown, and warnings for the given resume.

    Returns 401 if not authenticated, 404 if resume id is invalid or not found.
    """
    if not _get_user_email():
        return jsonify({"success": False}), 401

    if not _is_valid_resume_id(resume_id):
        return jsonify({"error": ERROR_RESUME_NOT_FOUND}), 404

    resume = resume_service.get_resume_by_id(resume_id)
    if not resume:
        return jsonify({"error": ERROR_RESUME_NOT_FOUND}), 404

    score, breakdown, warnings = calculate_resume_score(resume)
    open_view("score")

    return jsonify({
        "score": score,
        "breakdown": breakdown,
        "warnings": warnings or [],
    })


@resume_bp.get("/skills/frequency")
def skill_frequency() -> Tuple[Response, int] | Response:
    """
    Return skill frequency data for the authenticated user.

    Returns 401 if not authenticated.
    """
    email = _get_user_email()
    if not email:
        return jsonify({}), 401

    freq = get_skill_frequency(email)
    return jsonify(freq)


@resume_bp.post("/navigation/open")
def open_nav() -> Tuple[Response, int] | Response:
    """
    Push a view onto the navigation stack.

    Expects JSON body with optional "view" key.
    """
    data = request.get_json(silent=True)
    view = data.get("view") if isinstance(data, dict) else None
    open_view(view)
    return jsonify({"status": "pushed", "view": view})


@resume_bp.post("/navigation/back")
def back_nav() -> Response:
    """Pop the current view from the navigation stack and return the new current view."""
    view = go_back()
    return jsonify({"status": "popped", "current": view})


@resume_bp.delete("/<resume_id>")
def delete_resume(resume_id: str) -> Tuple[Response, int] | Response:
    """
    Delete a resume by id for the authenticated user.

    Returns 401 if not authenticated, 404 if resume id is invalid or not owned by user.
    """
    email = _get_user_email()
    if not email:
        return jsonify({"success": False, "message": "Unauthorized"}), 401

    if not _is_valid_resume_id(resume_id):
        return jsonify({"success": False, "message": MSG_RESUME_NOT_FOUND_OR_NOT_ALLOWED}), 404

    success = resume_service.delete_resume(email, resume_id)
    if not success:
        return jsonify({
            "success": False,
            "message": MSG_RESUME_NOT_FOUND_OR_NOT_ALLOWED,
        }), 404

    resume_logger.info("Resume deleted successfully")
    return jsonify({
        "success": True,
        "message": "Resume deleted successfully",
    })
