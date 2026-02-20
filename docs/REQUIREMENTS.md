# requirements.txt – Description and Where Each Package Is Used

Every line in `requirements.txt` (1–34) with a short description and where it is used in this project.

---

| # | Package | Version | What it does | Where it's used |
|---|---------|---------|--------------|------------------|
| 1 | **Authlib** | 1.6.7 | OAuth 2.0 / OpenID Connect client | **Python/Controller/google_controller.py** – `from authlib.integrations.flask_client import OAuth`. Used for Google login (register provider, authorize_redirect, authorize_access_token, parse_id_token). |
| 2 | **blinker** | 1.9.0 | Lightweight signaling (observer pattern) | **Not used directly.** Required by Flask (and Flask-Mail) for signals (e.g. `message_sent` when email is sent). Used under the hood when `mail.send()` is called. |
| 3 | **certifi** | 2026.1.4 | Mozilla CA bundle for SSL/TLS verification | **Not used directly.** Used by **requests** and **urllib3** when making HTTPS calls (admin UI → API, OpenAI, Google OAuth, chat_service, test_openai). |
| 4 | **cffi** | 2.0.0 | C Foreign Function Interface | **Not used directly.** Dependency of **cryptography** (C extensions for crypto). |
| 5 | **charset-normalizer** | 3.4.4 | Character encoding detection | **Not used directly.** Dependency of **requests** when decoding response content. |
| 6 | **click** | 8.3.1 | CLI framework | **Not used directly.** Used by **Flask** for CLI commands (e.g. `flask run`). |
| 7 | **colorama** | 0.4.6 | Colored terminal output (Windows) | **Not used directly.** Often used by **pytest** / terminal tools for colored output. |
| 8 | **cryptography** | 46.0.4 | Cryptographic primitives (C backend) | **Not used directly.** Used by **itsdangerous** (and related security) for secure signing/encoding of tokens. |
| 9 | **dnspython** | 2.8.0 | DNS toolkit | **Not used directly.** Dependency of **Redis** or email (SMTP) connection logic. |
| 10 | **Flask** | 3.1.2 | Web framework | **Python/app.py** (create_app, Flask()), all **Controller/** files (Blueprint, request, jsonify, session, redirect, url_for, etc.), **run.py**. Core of the backend. |
| 11 | **flask-cors** | 6.0.2 | Cross-Origin Resource Sharing | **Python/app.py** – `from flask_cors import CORS` and `CORS(app, ...)`. Allows frontend (different origin) to call the API. |
| 12 | **Flask-Mail** | 0.10.0 | Email sending from Flask | **Python/utils/mail_utils.py** – `from flask_mail import Mail`; **Controller/forgot_password_controller.py** – `from flask_mail import Message`, `mail.send(msg)`. Forgot-password and contact/email flows. |
| 13 | **idna** | 3.11 | Internationalized domain names | **Not used directly.** Dependency of **requests** for URL handling. |
| 14 | **itsdangerous** | 2.2.0 | Secure token signing (e.g. reset links) | **Python/Controller/reset_password_controller.py** – `URLSafeTimedSerializer`, `BadSignature`, `SignatureExpired`; **Controller/forgot_password_controller.py** – `URLSafeTimedSerializer`. Sign/verify reset-password tokens. |
| 15 | **Jinja2** | 3.1.6 | Template engine | **Not used directly.** Used by **Flask** for server-side templates (if any). |
| 16 | **MarkupSafe** | 3.0.3 | Safe string handling for templates | **Not used directly.** Dependency of **Jinja2**. |
| 17 | **pycparser** | 3.0 | C parser used by cffi | **Not used directly.** Dependency of **cffi**. |
| 18 | **pymongo** | 4.16.0 | MongoDB driver | **Python/config/db.py** – `from pymongo import MongoClient`; **repo/user_repo.py**, **repo/resume_repo.py** use `db` (from config). All user, resume, feedback data. |
| 19 | **python-dotenv** | 1.2.1 | Load `.env` into environment | **Python/app.py**, **config/db.py**, **config/openai_config.py**, **config/redis_config.py**, **Controller/contact_email_controller.py**, **test_openai.py**, **test.py** – `load_dotenv()`. Load MONGODB_URI, REDIS_URL, OPENAI_API_KEY, etc. |
| 20 | **redis** | 7.1.0 | Redis client | **Python/config/redis_config.py** – `import redis`, `redis.Redis(...)`; **utils/rate_limiter.py** (rate limiting); **services/chat_service.py** (cache). |
| 21 | **requests** | 2.32.5 | HTTP client | **admin/** – all sections (dashboard, users, resumes, analytics, chatbot, system, logs) call Flask API; **Python/services/chat_service.py** (OpenAI HTTP); **Python/test_openai.py**. |
| 22 | **streamlit** | ≥1.28.0 | Dashboard / data app framework | **admin/admin_app.py**, **admin/sections/*.py** – `import streamlit as st`. Entire admin UI (login, sidebar, pages). |
| 23 | **pandas** | ≥2.0.0 | DataFrames and tabular data | **admin/sections/dashboard.py**, **users.py**, **resumes.py**, **analytics.py** – `import pandas as pd`. Tables and chart data. |
| 24 | **plotly** | ≥5.0.0 | Interactive charts | **admin/sections/analytics.py** – `import plotly.express as px` (line/bar charts for users over time, resumes over time, top users). |
| 25 | **urllib3** | 2.6.3 | HTTP client (low-level) | **Not used directly in app code.** Used by **requests** for HTTP. (Note: `urllib.parse` in redis_config is stdlib, not this package.) |
| 26 | **Werkzeug** | 3.1.5 | WSGI utilities, routing, security | **Flask** core. **Python/services/user_service.py** – `generate_password_hash`, `check_password_hash`; **Controller/admin_service** – `check_password_hash`; **Controller/reset_password_controller** – `generate_password_hash`; **Controller/ats_controller** – `secure_filename`. |
| 27 | **gunicorn** | ≥21.0.0 | Production WSGI server | **Not used in code.** Used in production (e.g. `gunicorn app:create_app()` or similar) to run the Flask app. |
| 28 | **pdfplumber** | ≥0.10.0 | Extract text from PDFs | **Python/services/ats_checker_service.py** – `import pdfplumber`, `pdfplumber.open(pdf_path)`, `page.extract_text()`. ATS check from uploaded PDF. |
| 29 | **spacy** | ≥3.7.0 | NLP (tokenization, POS, entities) | **Python/services/ats_checker_service.py** – `import spacy`, `nlp = spacy.load("en_core_web_sm")`, `_extract_keywords()` (nouns, noun chunks). Keyword extraction for resume vs job description. |
| 30 | **scikit-learn** | ≥1.3.0 | ML / text vectorization and similarity | **Python/services/ats_checker_service.py** – `TfidfVectorizer`, `cosine_similarity` for resume–JD keyword similarity in ATS scoring. |
| 31 | **openai** | ≥1.0.0 | OpenAI API client | **Python/services/ats_checker_service.py** – `from openai import OpenAI` (suggestions); **utils/openai_client.py**; **ai/resume_generator.py** (AI resume, role suggestions); **api/admin/chatbot.py** (admin Q&A). |
| 32 | **pytest** | ≥7.0.0 | Test runner | **tests/** – run tests (`pytest tests/`). Not imported in main app. |
| 33 | **pytest-cov** | ≥4.0.0 | Pytest coverage plugin | **Tests** – `pytest --cov` for code coverage. Not imported in main app. |
| 34 | **coverage** | ≥7.0.0 | Coverage measurement | **Tests/reports** – used with pytest-cov and **.coveragerc** for coverage reports. Not imported in main app. |

---

## Summary by role

- **Web / API:** Flask, flask-cors, Werkzeug, Jinja2, MarkupSafe, click, gunicorn  
- **Auth / security:** Authlib (Google), itsdangerous (tokens), cryptography, Werkzeug (passwords)  
- **Data:** pymongo, redis  
- **Email:** Flask-Mail, blinker (signals)  
- **Env / HTTP:** python-dotenv, requests, urllib3, certifi, charset-normalizer, idna  
- **Admin UI:** streamlit, pandas, plotly  
- **AI:** openai  
- **ATS (resume vs JD):** pdfplumber, spacy, scikit-learn, openai  
- **Testing:** pytest, pytest-cov, coverage, colorama  
- **Low-level deps:** cffi, pycparser (cryptography), dnspython (Redis/mail)

All paths above are relative to the project root. “Not used directly” means the package is only used by another dependency, not by your own source code.
