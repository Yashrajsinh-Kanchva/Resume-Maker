# Python Backend – Full Reference

This document describes the **Python** backend: tech stack, directory layout, each module’s role, and how they fit together. No code is modified here—information only.

---

## 1. Tech Stack & Dependencies

| Category | Technology | Purpose |
|----------|------------|---------|
| **Web framework** | Flask 3.x | HTTP server, blueprints, sessions, request/response |
| **Database** | MongoDB (PyMongo) | Users, resumes, feedbacks; `MONGODB_URI` → `resume_app` DB |
| **Cache / rate limit** | Redis | Rate limiting, chat metrics, optional session/cache |
| **Auth** | Authlib (OAuth 2 / OIDC) | Google sign-in; `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET` |
| **AI** | OpenAI API (`openai` package) | Resume generation, role suggestions, chat; `OPENAI_API_KEY`, `OPENAI_MODEL` |
| **Email** | Flask-Mail | Forgot password, reset link, contact form |
| **Security** | Werkzeug (password hashing), custom CryptoUtils (base64 encode/decode for local user fields) | Passwords hashed; local email/name encoded in DB |
| **CORS** | flask-cors | Allow frontend origin to call API |
| **Env** | python-dotenv | Load `.env` (Mongo, Redis, OpenAI, Flask secret, OAuth) |
| **Production** | Gunicorn | WSGI server (see `requirements.txt`) |
| **Other** | requests, pdfplumber, spacy, scikit-learn | ATS parsing, NLP, scoring (as used by services) |

All of the above are reflected in **requirements.txt** at project root (Flask, pymongo, redis, openai, Authlib, Flask-Mail, cryptography, pytest, etc.).

---

## 2. Directory Structure (High Level)

```
Python/
├── app.py              # Application factory: create_app(), config, CORS, blueprints
├── run.py              # Dev entry: runs Flask on host/port from env
├── config/             # App config, MongoDB, Redis, OpenAI
├── Controller/         # Flask blueprints and route handlers
├── services/           # Business logic (user, resume, admin, chat, ATS, skills, AI resume)
├── repo/               # Data access (user_repo, resume_repo → MongoDB collections)
├── utils/              # Shared helpers (crypto, logger, validators, mail, rate limit, cache, intent)
├── api/                # API submodules (e.g. admin chatbot)
│   └── admin/          # Admin chatbot (rule-based + OpenAI)
├── DTO/                # Data transfer objects (user signup/login, chat)
├── ai/                 # AI prompts and resume generation (OpenAI)
└── DS/                 # Data structures (Stack, PriorityQueue, HashMap, Trie)
```

Imports assume **Python** is on the path (e.g. `PYTHONPATH=Python`). Example: `from Controller.user_controller import user_bp`, `from config.db import db`, `from services.user_service import UserService`.

---

## 3. Config (`config/`)

| File | Role |
|------|------|
| **app_config.py** | `Config` class: `SECRET_KEY`, Google OAuth env vars, session cookie settings (`HTTPONLY`, `SAMESITE`). Path constants: `BASE_DIR`, `FSD_DIR`, `HTML_DIR`, `CSS_DIR`, `JS_DIR`, `IMG_DIR` for frontend static files. |
| **db.py** | Loads `MONGODB_URI` from env, creates PyMongo `MongoClient`, exposes `db = client["resume_app"]`. Helpers: `get_users_collection()`, `get_feedback_collection()` returning `db["users"]` and `db["feedbacks"]`. |
| **redis_config.py** | Parses `REDIS_URL`, creates `redis_client` (Redis connection with `decode_responses=True`) for rate limiting and chat. |
| **openai_config.py** | Loads `OPENAI_API_KEY`, `OPENAI_MODEL` (default `gpt-4o-mini`). Builds `OPENAI_HEADERS` and `OPENAI_URL` for chat completions. |

---

## 4. Controllers (`Controller/`)

All are Flask **blueprints** registered in `app.py`. URL prefixes are set in `app.py` unless noted in the table.

| File | Blueprint | URL / Routes | Purpose |
|------|-----------|--------------|---------|
| **page_controller.py** | page_bp | `/`, `/login`, `/dashboard`, `/contact`, `/settings`, `/documents`, `/logout`, `/reset-password/<token>`, `/forgot-password.html`, `/choose-template.html`, `/step-1.html` … `/step-4.html`, `/build-resume.html`, `/navbar.html`, `/feedback.html`, `/about.html`, etc. | Serve HTML pages and static routes; session-based redirects for auth. |
| **user_controller.py** | user_bp | Prefix `/api/users`. `/me`, `/profile` (GET/PUT), `/login` (POST), signup (POST). | User auth (login/signup), profile read/update, session. |
| **google_controller.py** | google_bp | Prefix `/api/auth/google`. `/login` (GET), `/callback` (GET). | Google OAuth: initiate login, handle callback, call `UserService.login_with_google`, set session, redirect to `/login-success`. |
| **chat_controller.py** | chat_api | Prefix `/api/chat`. POST `/`. | Chat API: rate limit, then `process_chat` (intent, cache, OpenAI). |
| **resume_controller.py** | resume_bp | Prefix `/api/resumes`. Routes for list, get, create, update, delete resumes; ranking; score; navigation stack; skill frequency; CSV export. | Full resume CRUD, ranking, scoring, ATS-related endpoints. |
| **ai_resume_controller.py** | ai_resume_bp | `/ai/suggest` (POST), `/ai/create-resume` (POST), `/api/profile/status` (GET). | AI role suggestions and AI-generated resume creation. |
| **skill_controller.py** | skill_bp | Prefix `/api/skills`. Suggest skills (e.g. by prefix). | Skill suggestions for resume builder. |
| **ats_controller.py** | ats_bp | Prefix `/api/ats`. `/check` (POST), `/check-from-resume` (POST). | ATS check (text or from resume), uses ATSCheckerService and resume score. |
| **admin_controller.py** | admin_bp | Prefix `/api/admin`. `/resumes`, `/analytics`, `/users`, `/users/block`, `/users/unblock`, `/users/delete`, `/login`, `/users/export`, `/resumes/export`, `/logs`. | Main admin API: list resumes/users, analytics, user block/unblock/delete, login, CSV exports, log file content. |
| **admin_data_controller.py** | admin_data_bp | Prefix `/api/admin`. `/dashboard`, `/users`, `/resumes`, `/health`. | Dashboard counts, health check; uses AdminDataService. |
| **admin_analytics_controller.py** | admin_analytics_bp | Prefix `/api/admin`. GET `/analytics`. | Analytics data (overlaps with admin_bp; admin_bp registered first). |
| **admin_user_action_controller.py** | admin_user_action_bp | Prefix `/api/admin`. POST `/users/block`, `/users/unblock`, `/users/delete`. | User actions (overlap with admin_bp). |
| **forgot_password_controller.py** | forgot_password_bp | POST `/forgot-password`. | Request password reset; send email with link. |
| **reset_password_controller.py** | reset_password_bp | GET/POST `/api/reset-password/<token>`. | Validate token, show form, set new password. |
| **feedback_controller.py** | feedback_bp | POST `/api/feedback`, GET `/api/feedbacks`. | Submit feedback, list feedbacks (e.g. for admin). |
| **contact_email_controller.py** | contact_api | Prefix `/api/contact`. POST `/send`. | Send contact form email. |

**api/admin/chatbot.py** (not under `Controller/`): Blueprint `chatbot_bp` registered under `/api/admin`. POST `/chatbot` — admin-only natural-language Q&A (rule-based + OpenAI); requires `X-Admin-Email` header.

---

## 5. Services (`services/`)

| File | Main exports / class | Purpose |
|------|----------------------|---------|
| **user_service.py** | UserService | Register, login (local + Google via `login_with_google`), profile update; uses UserRepo and CryptoUtils for local users. |
| **resume_service.py** | ResumeService | Create/read/update/delete resumes, list by user, `get_all_resumes_for_admin`; uses ResumeRepo, CryptoUtils. |
| **admin_service.py** | AdminService | `get_all_users`, block/unblock/delete user, `login_admin`, `is_admin(email)`; uses UserRepo, CryptoUtils. |
| **admin_data_service.py** | AdminDataService | `dashboard()` (counts, providers), `users()`, `resumes()` aggregation, `health()` (flask/mongo/redis). |
| **admin_analytics_service.py** | AdminAnalyticsService | `get_analytics()`: users_over_time, resumes_over_time, top_users (MongoDB aggregations). |
| **admin_user_action_service.py** | AdminUserActionService | block_user, unblock_user, delete_user (used by admin_user_action_controller). |
| **chat_service.py** | process_chat | Intent detection, semantic cache (Redis), OpenAI fallback; rate-limit metrics. |
| **ai_resume_service.py** | create_ai_resume | Merge user payload with AI output (prompts from ai/prompts), build resume data; uses ResumeRepo, UserRepo. |
| **resume_score_service.py** | calculate_resume_score, _validate_resume_data | Score resume sections (profile, summary, skills, experience, education, projects, ATS keywords); validation for step data. |
| **resume_ranking_service.py** | rank_resumes | Rank resumes (e.g. by score). |
| **ats_checker_service.py** | ATSCheckerService | ATS check: extract text from resume steps, compare with job description; TF-IDF / overlap logic; suggestions. |
| **skill_suggestion_service.py** | suggest_skills | Suggest skills (e.g. prefix-based). |
| **skill_frequency_service.py** | get_skill_frequency | Skill frequency for a user (from resumes). |
| **navigation_stack_service.py** | open_view, go_back, current_view | In-memory stack (DS.stack) for resume builder navigation. |

---

## 6. Repositories (`repo/`)

| File | Role |
|------|------|
| **user_repo.py** | UserRepo: MongoDB `db["users"]` — find_by_email, find_all, insert, update, delete. Used by UserService, AdminService. |
| **resume_repo.py** | ResumeRepo: MongoDB `db["resumes"]` — find by user, find all, insert, update, delete. Used by ResumeService, AiResumeService. |

---

## 7. Utils (`utils/`)

| File | Role |
|------|------|
| **crypto_utils.py** | CryptoUtils: base64 encode/decode with secret wrapper (for storing local user email/name encoded in DB). safe_decode for tolerant decode. |
| **validators.py** | is_valid_gmail(email), validate_password(password) — format and strength checks. |
| **logger.py** | LineRotatingFileHandler (line-based log rotation), setup_logger(name, log_file), LOG_DIR; used by admin, resume, ATS controllers/services. |
| **mail_utils.py** | Flask-Mail init (init_mail(app)); used for forgot/reset password and contact. |
| **rate_limiter.py** | is_rate_limited(client_id) — Redis-based; used by chat to limit requests. |
| **semantic_cache.py** | semantic_key(text) — build cache key for chat responses (Redis). |
| **intent_mapper.py** | detect_intent(text), is_website_question(text) — classify user intent for chat. |
| **openai_client.py** | call_openai(prompt) — wrapper for OpenAI API (used where needed outside chat_service). |

---

## 8. DTOs (`DTO/`)

| File | Role |
|------|------|
| **user_signup_dto.py** | UserSignupDTO(name, email, password): validation (is_valid), to_dict for DB. |
| **user_login_dto.py** | UserLoginDTO: login payload validation / shape. |
| **chat_dto.py** | Chat request/response DTOs for chat API. |

---

## 9. AI (`ai/`)

| File | Role |
|------|------|
| **prompts.py** | build_resume_prompt(user_data), build_role_suggestions_prompt(role) — strict prompts for JSON resume output and role-based title/summary/skills/job_description. |
| **resume_generator.py** | Uses OpenAI client and prompts: suggest_from_role(role), generate_ai_resume(user_data); parses JSON from model output. Called by ai_resume_controller and ai_resume_service. |

---

## 10. Data Structures (`DS/`)

| File | Role |
|------|------|
| **stack.py** | Stack (push, pop, peek, is_empty, size) — used by navigation_stack_service. |
| **priority_queue.py** | Priority queue implementation. |
| **hashmap.py** | HashMap implementation. |
| **trie.py** | Trie implementation (e.g. for autocomplete/skills). |

---

## 11. API – Admin (`api/admin/`)

| File | Role |
|------|------|
| **chatbot.py** | Blueprint `chatbot_bp`, route POST `/chatbot`. Requires `X-Admin-Email`; checks AdminService.is_admin(email). Rule-based answers (e.g. total users, resumes, feedbacks, average rating) + OpenAI fallback. Read-only MongoDB access. Returns JSON with `answer` and headers (e.g. X-Chatbot-Build, X-Chatbot-Mode). |

---

## 12. Application Bootstrap (`app.py`, `run.py`)

- **app.py**: `create_app(config_class=Config)` — creates Flask app, loads Config, validates required env, configures session security (HTTPONLY, SAMESITE), CORS, mail, Redis/OAuth init, registers all blueprints. Page routes first, then user/auth, password, resume, AI, skills, ATS, chat, contact, feedback, admin (admin_bp, admin_data_bp, admin_analytics_bp, admin_user_action_bp, chatbot_bp under `ADMIN_API_PREFIX`).
- **run.py**: Imports `create_app`, runs `app.run(host, port, debug)` from env (`FLASK_HOST`, `FLASK_PORT`, `FLASK_DEBUG`). Used for local dev; production uses a WSGI server (e.g. Gunicorn) with `app:create_app()`.

---

## 13. Environment Variables (Summary)

| Variable | Purpose |
|----------|---------|
| MONGODB_URI | MongoDB connection string; required. |
| REDIS_URL | Redis connection URL; used by rate_limiter and chat. |
| FLASK_SECRET_KEY | Flask session signing; default dev key if unset. |
| FLASK_HOST, FLASK_PORT, FLASK_DEBUG | Dev server (run.py). |
| GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET | Google OAuth. |
| OPENAI_API_KEY | OpenAI API; required for AI resume and chat. |
| OPENAI_MODEL | Model name (default gpt-4o-mini). |
| (Mail) MAIL_*, SMTP_* etc. | Used by Flask-Mail for forgot/reset password and contact. |

---

## 14. Request Flow (Conceptual)

1. **HTTP** → Flask (run.py or WSGI).
2. **Routing** → Blueprint (Controller or api/admin).
3. **Controller** → Calls one or more **services** (and sometimes **repo** or **utils**).
4. **Services** → Use **repo** (MongoDB), **utils** (crypto, logger, validators), **config** (db, redis, openai), and sometimes **ai** (prompts, resume_generator).
5. **Response** → JSON or redirect or file/HTML from Controller.

Admin Streamlit app (separate process) calls the same Flask API under `/api/admin` (login, dashboard, users, resumes, analytics, chatbot, health, logs).

---

This is the full picture of the Python backend: tech used, layout, and what each file does.
