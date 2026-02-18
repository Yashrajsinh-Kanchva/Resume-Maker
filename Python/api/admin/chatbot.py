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
CHATBOT_BUILD = "2026-02-17-feedback-rules-v2"

def _respond(answer: str, *, status: int = 200, mode: str = "rule"):
    resp = jsonify({"answer": answer})
    resp.headers["X-Chatbot-Build"] = CHATBOT_BUILD
    resp.headers["X-Chatbot-Mode"] = mode
    return resp, status

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


def _rule_total_feedbacks(_q: str) -> str | None:
    n = db["feedbacks"].count_documents({})
    entry_word = "entry" if n == 1 else "entries"
    return f"There are {n} feedback {entry_word}."


def _extract_feedback_name(q: str) -> str:
    """
    Extract a name from questions like:
    - 'give me the feedback where name is mihir'
    - 'how many feedback have mihir name'
    - 'feedback with name mihir'
    - 'feedback by mihir'
    - 'feedback like mihir'

    Note: patterns are Unicode-aware to support international names.
    """
    # Unicode-aware: \w matches letters/digits in many scripts in Python 3 (re.UNICODE default).
    # Allow common name punctuation and spaces: . ' ’ -
    name_group = r"([\w\s\.'’\-]{1,60})"
    patterns = [
        rf"(?:name\s+is|named)\s+{name_group}",
        rf"(?:with\s+name)\s+{name_group}",
        rf"(?:where)\s+name\s*(?:is|=)\s*{name_group}",
        rf"(?:have|has)\s+{name_group}\s+name",
        rf"(?:feedbacks?\s+(?:from|by)\s+){name_group}",
        rf"(?:like)\s+{name_group}",
    ]
    for pat in patterns:
        m = re.search(pat, q)
        if m:
            return (m.group(1) or "").strip()
    return ""


def _rule_feedbacks_by_name(q: str) -> str | None:
    name = _extract_feedback_name(q)
    if not name:
        return None

    # Read-only query; exclude email to reduce sensitive output.
    regex = re.compile(re.escape(name), re.IGNORECASE)
    query = {"name": {"$regex": regex}}

    count = db["feedbacks"].count_documents(query)
    if count == 0:
        return f"No feedback entries found for name containing '{name}'."

    docs = list(
        db["feedbacks"]
        .find(query, {"_id": 0, "email": 0})
        .sort("created_at", -1)
        .limit(5)
    )

    shown = len(docs)
    entry_word = "entry" if count == 1 else "entries"
    lines = [
        f"Found {count} feedback {entry_word} matching name '{name}'. Showing latest {shown}:"
    ]

    for d in docs:
        person = d.get("name", "Unknown")
        rating = d.get("rating", "N/A")
        text = (d.get("feedback") or "").strip()
        created_at = d.get("created_at")
        created_s = ""
        if created_at is not None:
            try:
                created_s = created_at.isoformat()
            except Exception:
                created_s = str(created_at)

        suffix = f" ({created_s})" if created_s else ""
        lines.append(f"- {person}: rating {rating} — {text}{suffix}")

    return "\n".join(lines)


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


def _asks_how_many(q: str) -> bool:
    return "how many" in q or re.search(r"\bhow\s+ma", q) is not None


def _asks_total(q: str) -> bool:
    return "total" in q or "count" in q or "registered" in q


def _has_feedback(q: str) -> bool:
    return (
        re.search(r"feed\s*back", q) is not None
        or (("feed" in q) and ("back" in q))
        or "feedback" in q
        or "feedb" in q
    )


def _has_user(q: str) -> bool:
    return "user" in q or "users" in q or "usr" in q


def _has_resume(q: str) -> bool:
    return "resume" in q or "resumes" in q or "cv" in q


def _match_rule(q: str) -> str | None:
    feedback_by_name = _rule_feedbacks_by_name(q)
    if feedback_by_name is not None:
        return feedback_by_name

    if _has_user(q) and (_asks_how_many(q) or _asks_total(q)):
        return _rule_total_users(q)
    if _has_resume(q) and (_asks_how_many(q) or _asks_total(q) or "exist" in q):
        return _rule_total_resumes(q)
    if _has_feedback(q) and (_asks_how_many(q) or _asks_total(q)):
        return _rule_total_feedbacks(q)
    if "average" in q and "rating" in q:
        return _rule_avg_rating(q)
    if ("analytics" in q or "admin" in q) and "summary" in q:
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


def _check_auth():
    """Return None if authorized, else (response, status, mode) for early return."""
    admin_email = (request.headers.get("X-Admin-Email") or "").strip()
    if not admin_email:
        try:
            print("[admin_chatbot] AUTH missing X-Admin-Email")
        except Exception:
            pass
        return _respond("Authorization required. Admin email header missing.", status=401, mode="auth")
    if not _admin_service.is_admin(admin_email):
        try:
            print(f"[admin_chatbot] AUTH denied email={admin_email!r}")
        except Exception:
            pass
        return _respond("Access denied. Not an admin.", status=403, mode="auth")
    return None


def _validate_question(question: str) -> tuple[str | None, tuple | None]:
    """Return (sanitized, None) if valid, else (None, (msg, status, mode)) for error response."""
    sanitized = _sanitize(question)
    if not sanitized:
        return None, ("Please ask a non-empty question.", 400, "validation")
    if len(question.strip()) > MAX_QUESTION_LENGTH:
        return None, ("Question is too long.", 400, "validation")
    return sanitized, None


def _get_answer_and_mode(sanitized: str) -> tuple[str, str]:
    """Compute answer text and mode (version, rule, or openai)."""
    if sanitized in {"version", "/version", "chatbot version", "debug version"}:
        return f"admin_chatbot build: {CHATBOT_BUILD}", "version"
    answer = _match_rule(sanitized)
    if answer is not None:
        return answer, "rule"
    return _openai_answer(sanitized), "openai"


@chatbot_bp.route("/chatbot", methods=["POST"])
def chatbot():
    try:
        print(f"[admin_chatbot] HIT build={CHATBOT_BUILD} ip={request.remote_addr} ua={request.headers.get('User-Agent','')[:80]!r}")
    except Exception:
        pass

    auth_response = _check_auth()
    if auth_response is not None:
        return auth_response

    data = request.get_json(silent=True) or {}
    sanitized, validation_error = _validate_question(data.get("question", ""))
    if validation_error is not None:
        return _respond(validation_error[0], status=validation_error[1], mode=validation_error[2])

    answer, mode = _get_answer_and_mode(sanitized)
    try:
        print(f"[admin_chatbot] OK build={CHATBOT_BUILD} mode={mode} q={sanitized!r}")
    except Exception:
        pass
    return _respond(answer, status=200, mode=mode)
