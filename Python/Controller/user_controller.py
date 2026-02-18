from flask import Blueprint, request, jsonify, redirect, session, url_for

from DTO.user_login_dto import UserLoginDTO
from DTO.user_signup_dto import UserSignupDTO
from services.user_service import UserService
from utils.validators import is_valid_gmail, validate_password
from utils.crypto_utils import CryptoUtils

user_bp = Blueprint("user", __name__)
user_service = UserService()


# ---------------- HEALTH CHECK ----------------
@user_bp.get("/hc")
def hc():
    return "done"


# ---------------- CURRENT USER ----------------
@user_bp.route("/me", methods=["GET"])
def get_me():
    if "user" not in session:
        return jsonify({"authenticated": False}), 401

    return jsonify({
        "authenticated": True,
        "user": session["user"]
    })


# ---------------- GET USER PROFILE ----------------
@user_bp.route("/profile", methods=["GET"])
def get_profile():
    if "user" not in session:
        return jsonify({"success": False, "message": "Unauthorized"}), 401
    
    try:
        user_email = session["user"]["email"]
        user_provider = session["user"].get("provider", "local")
        
        # Get user from database
        if user_provider == "local":
            encoded_email = CryptoUtils.encode(user_email)
        else:
            encoded_email = user_email
        
        user = user_service.repo.find_user_by_email(encoded_email)
        
        if not user:
            return jsonify({"success": False, "message": "User not found"}), 404
        
        # Decode name based on provider
        if user.get("provider") == "local":
            name = CryptoUtils.decode(user.get("name", ""))
        else:
            name = user.get("name", "")
        
        return jsonify({
            "success": True,
            "user": {
                "name": name,
                "email": user_email,
                "provider": user.get("provider", "local")
            }
        }), 200
        
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# ---------------- UPDATE USER PROFILE ----------------
@user_bp.route("/profile", methods=["PUT"])
def update_profile():
    if "user" not in session:
        return jsonify({"success": False, "message": "Unauthorized"}), 401
    
    try:
        data = request.get_json()
        new_name = data.get("name", "").strip()
        
        if not new_name:
            return jsonify({"success": False, "message": "Name is required"}), 400
        
        if len(new_name) < 2:
            return jsonify({"success": False, "message": "Name must be at least 2 characters long"}), 400
        
        user_email = session["user"]["email"]
        user_provider = session["user"].get("provider", "local")
        
        # Get user from database
        if user_provider == "local":
            encoded_email = CryptoUtils.encode(user_email)
        else:
            encoded_email = user_email
        
        user = user_service.repo.find_user_by_email(encoded_email)
        
        if not user:
            return jsonify({"success": False, "message": "User not found"}), 404
        
        # Update name with encryption based on provider
        if user.get("provider") == "local":
            # Encrypt name for local users
            encoded_name = CryptoUtils.encode(new_name)
            update_data = {"name": encoded_name}
        else:
            # Plain text for Google users
            update_data = {"name": new_name}
        
        # Update in database
        result = user_service.repo.update_user(
            {"email": encoded_email},
            {"$set": update_data}
        )
        
        if result.modified_count == 0:
            return jsonify({"success": False, "message": "Failed to update profile"}), 500
        
        # Update session - reassign entire dict to ensure Flask detects the change
        session["user"] = {
            "name": new_name,
            "email": user_email,
            "provider": user.get("provider", "local")
        }
        # Explicitly mark session as modified
        session.modified = True
        
        return jsonify({
            "success": True,
            "message": "Profile updated successfully",
            "user": {
                "name": new_name,
                "email": user_email,
                "provider": user.get("provider", "local")
            }
        }), 200
        
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# ---------------- SIGNUP ----------------
@user_bp.post("/signup")
def signup():
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")
    confirm = request.form.get("confirm_password")

    if not all([name, email, password, confirm]):
        return jsonify({"success": False, "message": "All fields are required"}), 400

    if not is_valid_gmail(email):
        return jsonify({
            "success": False,
            "message": "Email must be a valid @gmail.com address"
        }), 400

    if password != confirm:
        return jsonify({
            "success": False,
            "message": "Passwords do not match"
        }), 400

    valid, message = validate_password(password)
    if not valid:
        return jsonify({
            "success": False,
            "message": message
        }), 400

    dto = UserSignupDTO(name, email, password)
    if not dto.is_valid():
        return jsonify({
            "success": False,
            "message": "Invalid signup data"
        }), 400

    result = user_service.create_user(dto)

    # ✅ AUTO LOGIN AFTER SUCCESSFUL SIGNUP
    if result.get("success"):
        session["user"] = {
            "name": name,
            "email": email,
            "provider": "local"
        }
        session.modified = True

        return jsonify({
            "success": True,
            "message": "Account created successfully!"
        }), 201

    return jsonify(result), 400

# ---------------- LOGIN (EMAIL / PASSWORD) ----------------
@user_bp.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")

    # ---------- Field check ----------
    if not email or not password:
        return jsonify({
            "success": False,
            "message": "Email and password are required"
        }), 400

    # ---------- Email validation ----------
    if not is_valid_gmail(email):
        return jsonify({
            "success": False,
            "message": "Only @gmail.com emails are allowed"
        }), 400

    # # ---------- Password format validation ----------
    # valid, _ = validate_password(password)
    # if not valid:
    #     return jsonify({
    #         "success": False,
    #         "message": "Invalid password format"
    #     }), 400

    # ---------- DTO ----------
    dto = UserLoginDTO(email=email, password=password)
    if not dto.is_valid():
        return jsonify({
            "success": False,
            "message": "Invalid login data"
        }), 400

    result = user_service.login_user(dto)

    # ❌ LOGIN FAILED
    if not result.get("success"):
        return jsonify(result), 401

    user = result["user"]

    # 🚫 GOOGLE USERS CANNOT LOGIN VIA PASSWORD
    if user.get("provider") == "google":
        return jsonify({
            "success": False,
            "message": "Please login using Google"
        }), 403

    # ✅ SESSION
    session["user"] = {
        "name": user["name"],
        "email": user["email"],
        "provider": "local"
    }

    return jsonify({
        "success": True,
        "message": "Login successful"
    }), 200

