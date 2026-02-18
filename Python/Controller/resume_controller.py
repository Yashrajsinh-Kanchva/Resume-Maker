from flask import Blueprint, request, jsonify, session
from services.resume_service import ResumeService
from services.resume_score_service import calculate_resume_score
from services.navigation_stack_service import open_view, go_back

resume_bp = Blueprint("resume", __name__)
resume_service = ResumeService()

@resume_bp.post("/")
def create_resume():
    if "user" not in session:
        return jsonify({"success": False, "message": "Unauthorized"}), 401

    data = request.get_json()
    result = resume_service.create_resume(
        session["user"]["email"],
        data
    )
    return jsonify(result)

from services.resume_ranking_service import rank_resumes

@resume_bp.get("/")
def get_resumes():
    if "user" not in session:
        return jsonify([]), 401

    resumes = resume_service.get_user_resumes(
        session["user"]["email"]
    )
    # 🔥 APPLY DS-BASED RANKING
    ranked_resumes = rank_resumes(
        resumes,
        session["user"]["email"]
    )
    open_view("documents")
    return jsonify(ranked_resumes)


@resume_bp.get("/<resume_id>")
def get_single_resume(resume_id):
    if "user" not in session:
        return jsonify({"success": False}), 401

    resume = resume_service.get_resume_by_id(resume_id)
    if not resume:
        return jsonify({"error": "Resume not found"}), 404

    return jsonify(resume)   # ✅ NOTHING ELSE


@resume_bp.get("/score/<resume_id>")
def get_resume_score(resume_id):
    if "user" not in session:
        return jsonify({"success": False}), 401

    resume = resume_service.get_resume_by_id(resume_id)

    if not resume:
        return jsonify({"error": "Resume not found"}), 404

    score, breakdown, warnings = calculate_resume_score(resume)

    open_view("score")  # 🔥 STACK USED HERE

    return jsonify({
        "score": score,
        "breakdown": breakdown,
        "warnings": warnings or []
    })


from services.skill_frequency_service import get_skill_frequency

@resume_bp.get("/skills/frequency")
def skill_frequency():
    if "user" not in session:
        return jsonify({}), 401

    freq = get_skill_frequency(session["user"]["email"])
    return jsonify(freq)

from services.navigation_stack_service import open_view, go_back

@resume_bp.post("/navigation/open")
def open_nav():
    view = request.json.get("view")
    open_view(view)
    return jsonify({"status": "pushed", "view": view})

@resume_bp.post("/navigation/back")
def back_nav():
    view = go_back()
    return jsonify({"status": "popped", "current": view})

@resume_bp.delete("/<resume_id>")
def delete_resume(resume_id):
    if "user" not in session:
        return jsonify({"success": False, "message": "Unauthorized"}), 401

    email = session["user"]["email"]

    success = resume_service.delete_resume(email, resume_id)

    if not success:
        return jsonify({
            "success": False,
            "message": "Resume not found or not allowed"
        }), 404

    return jsonify({
        "success": True,
        "message": "Resume deleted successfully"
    })

