"""
Admin chatbot: natural-language questions about users, resumes, feedback.
Rule-based fast responses + OpenAI fallback. Read-only MongoDB access only.
Requires X-Admin-Email header for an authenticated admin.
"""
import re
from flask import Blueprint, request, jsonify
from config.db import db
from utils.openai_client import client
from services.admin_service import AdminService

chatbot_bp = Blueprint("admin_chatbot", __name__)
_admin_service = AdminService()

MAX_QUESTION_LENGTH = 2000
OPENAI_TIMEOUT = 10

SYSTEM_PROMPT = """You are an admin analytics helper with read-only access to MongoDB.
You may only answer questions about analytics and summaries. Do not perform write operations, deletions, or return sensitive data (passwords, tokens).

MongoDB database: resume_app. Collections and allowed fields (never expose or use password fields):
- users: name, email, provider, role, status, created_at
- resumes: user_email, title, created_at
- feedbacks: name, email, rating, feedback, created_at

Answer in short, human-readable sentences. Do not output raw JSON or code unless the user explicitly asks for schema or structure only.
If the question cannot be answered from these collections, say so briefly."""


def _sanitize(question: str) -> str:
    if not question or not isinstance(question, str):
        return ""
    s = question.strip().lower()
    s = re.sub(r"\s+", " ", s)
    return s[:MAX_QUESTION_LENGTH]


def _rule_total_users(_q: str) -> str | None:
    n = db["users"].count_documents({})
    return f"There are {n} users registered."


def _rule_total_resumes(_q: str) -> str | None:
    n = db["resumes"].count_documents({})
    return f"There are {n} resumes."


def _rule_avg_rating(_q: str) -> str | None:
    cursor = list(
        db["feedbacks"].aggregate([
            {"$group": {"_id": None, "avg": {"$avg": "$rating"}}}
        ])
    )
    if not cursor:
        return "There is no feedback yet, so no average rating."
    avg = cursor[0].get("avg")
    if avg is None:
        return "There is no feedback yet, so no average rating."
    return f"The average feedback rating is {avg:.1f}."


def _rule_analytics_summary(_q: str) -> str | None:
    users = db["users"].count_documents({})
    resumes = db["resumes"].count_documents({})
    feedbacks = db["feedbacks"].count_documents({})
    cursor = list(
        db["feedbacks"].aggregate([
            {"$group": {"_id": None, "avg": {"$avg": "$rating"}}}
        ])
    )
    avg_rating = cursor[0].get("avg") if cursor else None
    parts = [
        f"Total users: {users}. Total resumes: {resumes}. Total feedbacks: {feedbacks}."
    ]
    if avg_rating is not None:
        parts.append(f" Average feedback rating: {avg_rating:.1f}.")
    return "".join(parts).strip()


def _match_rule(q: str) -> str | None:
    if "user" in q and ("how many" in q or "total" in q or "registered" in q):
        return _rule_total_users(q)
    if "resume" in q and ("how many" in q or "total" in q or "exist" in q):
        return _rule_total_resumes(q)
    if "average" in q and "rating" in q:
        return _rule_avg_rating(q)
    if "analytics" in q and "summary" in q:
        return _rule_analytics_summary(q)
    if "admin" in q and "summary" in q:
        return _rule_analytics_summary(q)
    return None


def _openai_answer(question: str) -> str:
    try:
        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": question},
            ],
            temperature=0.3,
            timeout=OPENAI_TIMEOUT,
        )
        return (res.choices[0].message.content or "").strip()
    except Exception:
        return "I couldn't process that. Try asking about user counts, resume counts, or feedback ratings."


@chatbot_bp.route("/chatbot", methods=["POST"])
def chatbot():
    admin_email = (request.headers.get("X-Admin-Email") or "").strip()
    if not admin_email:
        return jsonify({"answer": "Authorization required. Admin email header missing."}), 401
    if not _admin_service.is_admin(admin_email):
        return jsonify({"answer": "Access denied. Not an admin."}), 403

    data = request.get_json(silent=True) or {}
    question = data.get("question", "")
    sanitized = _sanitize(question)

    if not sanitized:
        return jsonify({"answer": "Please ask a non-empty question."}), 400

    if len(question.strip()) > MAX_QUESTION_LENGTH:
        return jsonify({"answer": "Question is too long."}), 400

    answer = _match_rule(sanitized)
    if answer is None:
        answer = _openai_answer(sanitized)

    return jsonify({"answer": answer}), 200
