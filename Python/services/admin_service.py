from werkzeug.security import check_password_hash
from repo.user_repo import UserRepo
from utils.crypto_utils import CryptoUtils


class AdminService:
    def __init__(self):
        self.repo = UserRepo()

    # ================= USERS =================
    def get_all_users(self):
        users = self.repo.find_all_users()
        result = []

        for u in users:
            provider = u.get("provider", "local")

            email = (
                CryptoUtils.decode(u["email"])
                if provider == "local"
                else u["email"]
            )

            name = (
                CryptoUtils.decode(u.get("name", ""))
                if provider == "local"
                else u.get("name", "")
            )

            result.append({
                "_id": str(u["_id"]),
                "email": email,
                "name": name,
                "provider": provider,
                "status": u.get("status", "active"),
                "role": u.get("role", "user")
            })

        return result

    # ================= BLOCK / UNBLOCK / DELETE =================
    def block_user(self, email):
        encoded = CryptoUtils.encode(email)
        return self.repo.update_user(
            {"email": {"$in": [email, encoded]}},
            {"$set": {"status": "blocked"}}
        )

    def unblock_user(self, email):
        encoded = CryptoUtils.encode(email)
        return self.repo.update_user(
            {"email": {"$in": [email, encoded]}},
            {"$set": {"status": "active"}}
        )

    def delete_user(self, email):
        encoded = CryptoUtils.encode(email)
        return self.repo.delete_user(
            {"email": {"$in": [email, encoded]}}
        )

    # ================= ADMIN LOGIN =================
    def login_admin(self, email, password):
        encoded_email = CryptoUtils.encode(email)
        user = self.repo.find_user_by_email(encoded_email)

        if not user:
            return {"success": False, "message": "Admin not found"}

        if user.get("role") != "admin":
            return {"success": False, "message": "Access denied"}

        if not check_password_hash(user.get("password", ""), password):
            return {"success": False, "message": "Invalid credentials"}

        return {
            "success": True,
            "admin": {
                "name": CryptoUtils.decode(user.get("name", "")),
                "email": CryptoUtils.decode(user.get("email", "")),
                "role": "admin"
            }
        }

    def _email_query(self, email):
        encoded = CryptoUtils.encode(email)
        user = self.repo.find_user_by_email(encoded)
        if user:
            return {"email": encoded}
        return {"email": email}

    def is_admin(self, email: str) -> bool:
        """Return True if the given email belongs to a user with role admin."""
        if not email or not email.strip():
            return False
        email = email.strip()
        encoded = CryptoUtils.encode(email)
        user = self.repo.find_user_by_email(encoded) or self.repo.find_user_by_email(email)
        return user is not None and user.get("role") == "admin"
