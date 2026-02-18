from flask import Blueprint, request, jsonify
from datetime import datetime, timezone
from config.db import get_feedback_collection

feedback_bp = Blueprint("feedback_bp", __name__)

@feedback_bp.route("/api/feedback", methods=["POST"])
def save_feedback():
    data = request.json

    name = data.get("name")
    email = data.get("email")
    rating = data.get("rating")
    message = data.get("message")

    if not all([name, email, rating, message]):
        return jsonify({"msg": "All fields are required"}), 400

    feedback_doc = {
        "name": name,
        "email": email,
        "rating": int(rating),
        "feedback": message,
        "created_at": datetime.now(timezone.utc)
    }

    collection = get_feedback_collection()
    collection.insert_one(feedback_doc)

    return jsonify({"msg": "Feedback saved successfully"}), 201

@feedback_bp.route("/api/feedbacks", methods=["GET"])
def get_feedbacks():
    collection = get_feedback_collection()

    feedbacks = list(
        collection.find(
            {},
            {"_id": 0, "name": 1, "feedback": 1}
        )
        .sort("created_at", -1)   # 🔥 latest first
        .limit(3)                 # 🔥 ONLY 3 REVIEWS
    )

    return jsonify(feedbacks), 200
