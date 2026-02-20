"""
Seed dummy users, resumes, and feedbacks with varied timestamps
so admin Analytics charts show realistic data.

Run from project root:
  cd Python && python scripts/seed_dummy_data.py   # Bash/cmd
  cd Python; python scripts/seed_dummy_data.py     # PowerShell

Or from Python folder:
  python scripts/seed_dummy_data.py

Requires: MONGODB_URI in .env
"""
import os
import sys
from datetime import datetime, timezone, timedelta
from random import choice, randint

# Ensure Python package root is on path when run as script
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_SCRIPT_DIR)
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

# Load .env from project root (one level above Python)
_project_root = os.path.dirname(_ROOT)
_dotenv = os.path.join(_project_root, ".env")
if os.path.isfile(_dotenv):
    from dotenv import load_dotenv
    load_dotenv(_dotenv)

from config.db import db
from utils.crypto_utils import CryptoUtils
from werkzeug.security import generate_password_hash


# ---------- Config: time range for dummy data (days back from now) ----------
DAYS_BACK = 45
# One admin user so you can still log in to admin (local, role=admin)
ADMIN_EMAIL = "admin@gmail.com"
ADMIN_PASSWORD = "Admin123!@#"  # change after first login if needed
ADMIN_NAME = "Admin User"


def _random_date_in_range(days_back: int, end: datetime = None) -> datetime:
    """Return a random datetime within the last `days_back` days."""
    end = end or datetime.now(timezone.utc)
    start = end - timedelta(days=days_back)
    delta = end - start
    sec = randint(0, max(0, int(delta.total_seconds())))
    return start + timedelta(seconds=sec)


def clear_all():
    """Remove all users, resumes, and feedbacks."""
    db["resumes"].delete_many({})
    db["feedbacks"].delete_many({})
    db["users"].delete_many({})
    print("Cleared: users, resumes, feedbacks.")


def seed_admin():
    """Insert one admin user (local) so you can log in to admin."""
    encoded_email = CryptoUtils.encode(ADMIN_EMAIL)
    if db["users"].find_one({"email": encoded_email}):
        print("Admin user already exists, skipping.")
        return
    doc = {
        "name": CryptoUtils.encode(ADMIN_NAME),
        "email": encoded_email,
        "password": generate_password_hash(ADMIN_PASSWORD),
        "provider": "local",
        "status": "active",
        "role": "admin",
        "created_at": datetime.now(timezone.utc),
    }
    db["users"].insert_one(doc)
    print(f"Created admin: {ADMIN_EMAIL} / {ADMIN_PASSWORD}")


def seed_users_and_resumes_and_feedbacks():
    """Insert dummy users, resumes, and feedbacks with spread timestamps."""

    # Dummy user definitions: (name, email, provider)
    # Use distinct emails; local users will have encoded email/name in DB.
    dummy_users = [
        ("Alice Smith", "alice.smith@example.com", "local"),
        ("Bob Jones", "bob.jones@example.com", "local"),
        ("Carol White", "carol.white@example.com", "google"),
        ("David Brown", "david.brown@example.com", "local"),
        ("Eve Davis", "eve.davis@example.com", "google"),
        ("Frank Miller", "frank.miller@example.com", "local"),
        ("Grace Lee", "grace.lee@example.com", "local"),
        ("Henry Wilson", "henry.wilson@example.com", "google"),
        ("Ivy Taylor", "ivy.taylor@example.com", "local"),
        ("Jack Moore", "jack.moore@example.com", "local"),
        ("Kate Clark", "kate.clark@example.com", "google"),
        ("Leo Lewis", "leo.lewis@example.com", "local"),
        ("Mia Walker", "mia.walker@example.com", "local"),
        ("Noah Hall", "noah.hall@example.com", "google"),
        ("Olivia Young", "olivia.young@example.com", "local"),
    ]

    templates = [
        "professionalBlue", "minimalElegant", "academicYellow",
        "blueCorporate", "softGreenMinimal", "darkElegant",
        "timelineResume", "boldRedAccent", "cardBased", "glassmorphism",
    ]

    # Minimal resume JSON (admin only needs title/user_email/created_at; data can be minimal)
    minimal_data = {
        "sections": [
            {"type": "heading", "content": "Dummy resume"},
            {"type": "experience", "items": [{"title": "Demo", "company": "Demo Co", "duration": "2020-2024"}]},
        ]
    }

    now = datetime.now(timezone.utc)
    inserted_users = []  # list of (encoded_email, name, provider) for resumes/feedbacks

    # ---------- Insert users with created_at spread over DAYS_BACK ----------
    for name, email, provider in dummy_users:
        created_at = _random_date_in_range(DAYS_BACK, now)
        if provider == "local":
            doc = {
                "name": CryptoUtils.encode(name),
                "email": CryptoUtils.encode(email),
                "password": generate_password_hash("UserPass1!@#"),
                "provider": "local",
                "status": "active",
                "role": "user",
                "created_at": created_at,
            }
            inserted_users.append((CryptoUtils.encode(email), name, provider))
        else:
            doc = {
                "name": name,
                "email": email,
                "provider": "google",
                "status": "active",
                "role": "user",
                "created_at": created_at,
            }
            inserted_users.append((email, name, provider))
        db["users"].insert_one(doc)

    print(f"Inserted {len(inserted_users)} dummy users.")

    # ---------- Insert resumes: multiple per user, created_at spread ----------
    resume_count = 0
    for encoded_email, name, _ in inserted_users:
        # Each user gets 1–4 resumes at random dates
        for _ in range(randint(1, 4)):
            created_at = _random_date_in_range(DAYS_BACK, now)
            title = f"{choice(templates)} - {created_at.strftime('%b %d, %Y')}"
            doc = {
                "user_email": encoded_email,
                "title": title,
                "template": choice(templates),
                "data": minimal_data,
                "created_at": created_at,
            }
            db["resumes"].insert_one(doc)
            resume_count += 1
    print(f"Inserted {resume_count} dummy resumes.")

    # ---------- Insert feedbacks: varied ratings and dates ----------
    feedback_entries = [
        ("John D.", "john.d@example.com", 5, "Great tool, helped me land an interview!"),
        ("Jane S.", "jane.s@example.com", 4, "Very useful. Minor UI tweaks would help."),
        ("Mike R.", "mike.r@example.com", 5, "ATS check is a game changer."),
        ("Sarah K.", "sarah.k@example.com", 3, "Good but export options could be better."),
        ("Tom P.", "tom.p@example.com", 5, "Clean templates, easy to use."),
        ("Anna L.", "anna.l@example.com", 4, "Liked the variety of templates."),
        ("Chris M.", "chris.m@example.com", 5, "Exactly what I needed for my job search."),
        ("Emma W.", "emma.w@example.com", 2, "Had some bugs on mobile."),
        ("James H.", "james.h@example.com", 4, "Solid product. Would recommend."),
        ("Lisa T.", "lisa.t@example.com", 5, "Best free resume builder I've used."),
        ("Dan B.", "dan.b@example.com", 4, "Quick and professional results."),
        ("Rachel F.", "rachel.f@example.com", 5, "Got my resume past ATS. Thank you!"),
        ("Kevin N.", "kevin.n@example.com", 3, "Good value. Support was slow."),
        ("Amy C.", "amy.c@example.com", 5, "Simple and effective."),
        ("Steve G.", "steve.g@example.com", 4, "Worth trying for anyone job hunting."),
    ]
    for name, email, rating, message in feedback_entries:
        created_at = _random_date_in_range(DAYS_BACK, now)
        doc = {
            "name": name,
            "email": email,
            "rating": rating,
            "feedback": message,
            "created_at": created_at,
        }
        db["feedbacks"].insert_one(doc)
    print(f"Inserted {len(feedback_entries)} dummy feedbacks.")


def main():
    print("Seed script: clear DB and insert dummy data (users, resumes, feedbacks).")
    clear_all()
    seed_admin()
    seed_users_and_resumes_and_feedbacks()
    print("Done. Log in to admin with:", ADMIN_EMAIL, "/", ADMIN_PASSWORD)


if __name__ == "__main__":
    main()
