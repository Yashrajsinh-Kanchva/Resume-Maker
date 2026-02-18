from flask import Blueprint, request, jsonify, session
from services.ai_resume_service import create_ai_resume
from repo.user_repo import UserRepo
from ai.resume_generator import suggest_from_role

ai_resume_bp = Blueprint("ai_resume", __name__)
user_repo = UserRepo()   # 🔥 THIS WAS MISSING


@ai_resume_bp.route("/ai/suggest", methods=["POST"])
def suggest_resume_from_role():
    """Suggest title, summary, skills, job description based on target role only."""
    if not session.get("user"):
        return jsonify({"error": "Not authenticated"}), 401
    data = request.get_json() or {}
    role = (data.get("role") or "").strip()
    if not role:
        return jsonify({"error": "role is required"}), 400
    try:
        suggestions = suggest_from_role(role)
        return jsonify(suggestions)
    except Exception as e:
        print("AI suggest error:", e)
        return jsonify({"error": str(e), "title": role, "summary": "", "skills": [], "job_description": ""}), 500


@ai_resume_bp.route("/ai/create-resume", methods=["POST"])
def create_resume_with_ai():
    payload = request.json
    user = session.get("user")
    print("AI PAYLOAD RECEIVED:", payload)

    if not user:
        return jsonify({"error": "Not authenticated"}), 401

    try:
        resume_id = create_ai_resume(user["email"], payload)
        return jsonify({"resumeId": resume_id})
    except Exception as e:
        print("AI CREATE ERROR:", e)
        return jsonify({"error": str(e)}), 500


@ai_resume_bp.route("/api/profile/status", methods=["GET"])
def profile_status():
    email = (session.get("user") or {}).get("email")
    user = user_repo.find_user_by_email(email) if email else None

    return jsonify({
        "education": bool(user.get("education")) if user else False,
        "skills": bool(user.get("skills")) if user else False,
        "projects": bool(user.get("projects")) if user else False
    })
