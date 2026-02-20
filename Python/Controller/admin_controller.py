"""
Admin API controller.

Handles admin-only endpoints: resumes list, analytics, users CRUD, login,
CSV exports, and log file retrieval. Log paths are resolved from a fixed
allowlist so paths are never constructed from user-controlled data.
"""

import csv
import io
from pathlib import Path
from typing import Optional, Tuple

from flask import Blueprint, Response, jsonify, request

from services.admin_analytics_service import AdminAnalyticsService
from services.admin_service import AdminService
from services.resume_service import ResumeService
from utils.crypto_utils import CryptoUtils
from utils.logger import LOG_DIR, setup_logger
from utils.validators import is_valid_email

# ================= LOGGER =================
admin_logger = setup_logger(name="ADMIN", log_file="admin.log")

# ================= BLUEPRINT & SERVICES =================
admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")
admin_service = AdminService()
resume_service = ResumeService()
analytics_service = AdminAnalyticsService()

# ================= LOG PATH CONSTANTS (no user input in path construction) =================
_LOGS_DIR = Path(LOG_DIR).resolve()
_ADMIN_LOG_PATH = _LOGS_DIR / "admin.log"
_SERVICE_LOG_PATH = _LOGS_DIR / "service.log"
_ATS_CONTROLLER_LOG_PATH = _LOGS_DIR / "ats_controller.log"
_ATS_CHECKER_LOG_PATH = _LOGS_DIR / "ats_checker.log"

MSG_INVALID_LOG_TYPE = "Invalid log type"
MSG_INVALID_LOG_PATH = "Invalid log path"
MSG_LOG_FILE_NOT_FOUND = "Log file not found"


def _resolve_log_path(type_param: str) -> Optional[Path]:
    """
    Return the resolved Path for an allowed log type, or None if not allowed.

    Paths are fixed constants; type_param is only used to select which constant
    to return, so no user-controlled value is used in path construction.
    """
    if type_param == "admin":
        return _ADMIN_LOG_PATH
    if type_param == "service":
        return _SERVICE_LOG_PATH
    if type_param == "ats_controller":
        return _ATS_CONTROLLER_LOG_PATH
    if type_param == "ats_checker":
        return _ATS_CHECKER_LOG_PATH
    return None


# ================= RESUMES =================


@admin_bp.route("/resumes", methods=["GET"])
def get_all_resumes_admin() -> Tuple[Response, int]:
    """Return all resumes for admin listing."""
    resumes = resume_service.get_all_resumes_for_admin()
    return jsonify({"success": True, "data": resumes}), 200


# ================= ANALYTICS =================


@admin_bp.route("/analytics", methods=["GET"])
def get_analytics() -> Tuple[Response, int]:
    """Return analytics data with top users' emails decoded for display."""
    data = analytics_service.get_analytics()
    decoded_top_users = []

    for u in data.get("top_users", []):
        encoded_email = u.get("_id")
        try:
            email = CryptoUtils.decode(encoded_email)
        except (ValueError, AttributeError):
            email = encoded_email

        decoded_top_users.append({
            "user_email": email,
            "count": u.get("count", 0),
        })

    data["top_users"] = decoded_top_users
    return jsonify(data), 200


# ================= USERS =================


@admin_bp.route("/users", methods=["GET"])
def get_users() -> Tuple[Response, int]:
    """Return all users for admin."""
    admin_logger.info("GET /api/admin/users called")
    users = admin_service.get_all_users()
    admin_logger.info("Fetched %d users", len(users))
    return jsonify(users), 200


@admin_bp.route("/users/block", methods=["POST"])
def block_user() -> Tuple[Response, int]:
    """Block a user by email."""
    email = request.json.get("email")
    admin_service.block_user(email)
    return jsonify({"success": True}), 200


@admin_bp.route("/users/unblock", methods=["POST"])
def unblock_user() -> Tuple[Response, int]:
    """Unblock a user by email."""
    email = request.json.get("email")
    admin_service.unblock_user(email)
    return jsonify({"success": True}), 200


@admin_bp.route("/users/delete", methods=["POST"])
def delete_user() -> Tuple[Response, int]:
    """Delete a user by email."""
    email = request.json.get("email")
    admin_service.delete_user(email)
    return jsonify({"success": True}), 200


# ================= ADMIN LOGIN =================


@admin_bp.route("/login", methods=["POST"])
def admin_login() -> Tuple[Response, int]:
    """Authenticate admin by email and password. Returns 400 on bad input, 401 on failure."""
    raw = request.json or {}
    email = (raw.get("email") or "").strip() if raw.get("email") is not None else ""
    password = raw.get("password")

    if not email or not password:
        return jsonify({
            "success": False,
            "message": "Email and password are required",
        }), 400

    if not is_valid_email(email):
        return jsonify({
            "success": False,
            "message": "Invalid email format",
        }), 400

    result = admin_service.login_admin(email, password)
    if not result.get("success"):
        return jsonify(result), 401

    return jsonify(result), 200


# ================= USERS CSV EXPORT =================


@admin_bp.route("/users/export", methods=["GET"])
def export_users_csv() -> Response:
    """Export users as CSV attachment."""
    users = admin_service.get_all_users()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Email", "Name", "Provider", "Status", "Role"])

    for u in users:
        writer.writerow([
            u.get("email"),
            u.get("name"),
            u.get("provider"),
            u.get("status"),
            u.get("role"),
        ])

    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=users.csv"},
    )


# ================= RESUMES CSV EXPORT =================


@admin_bp.route("/resumes/export", methods=["GET"])
def export_resumes_csv() -> Response:
    """Export resumes list as CSV attachment."""
    data = resume_service.get_all_resumes_for_admin()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Email", "Title", "Created At"])

    for r in data:
        writer.writerow([
            r.get("email", ""),
            r.get("title", ""),
            r.get("created_at", ""),
        ])

    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=resumes.csv"},
    )


# ================= LOGS =================


@admin_bp.route("/logs", methods=["GET"])
def get_logs() -> Tuple[Response, int]:
    """
    Return the last 200 lines of a log file.

    Query param 'type' selects which log: admin, service, ats_controller, ats_checker.
    Returns 400 for invalid type or path check failure, 404 if file not found.
    """
    type_param = request.args.get("type", "admin")
    log_path = _resolve_log_path(type_param)

    if log_path is None:
        return jsonify({"success": False, "message": MSG_INVALID_LOG_TYPE}), 400

    if log_path.parent != _LOGS_DIR:
        return jsonify({"success": False, "message": MSG_INVALID_LOG_PATH}), 400

    if not log_path.is_file():
        return jsonify({"success": False, "message": MSG_LOG_FILE_NOT_FOUND}), 404

    with log_path.open("r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()[-200:]

    return jsonify({"success": True, "logs": lines}), 200
