# Python backend

Flask application and supporting code for the Resume Maker app. Run from **project root** with `PYTHONPATH=Python` (or run `python run.py` from this directory).

## Layout

| Directory    | Purpose |
| ------------| ------- |
| `Controller/` | Flask blueprints and route handlers (user, resume, admin, OAuth, etc.) |
| `config/`     | App config, MongoDB (`db`), Redis, OpenAI |
| `services/`  | Business logic (user, resume, admin, chat, ATS, skills, etc.) |
| `repo/`      | Data access (user_repo, resume_repo) |
| `utils/`     | Shared utilities (crypto, logger, validators, rate_limiter, etc.) |
| `api/`       | API modules (e.g. `api/admin/chatbot`) |
| `DTO/`       | Data transfer objects |
| `ai/`        | AI/resume generation and prompts |
| `DS/`        | Data structures (stack, priority queue, etc.) |

## Entry points

- **Development:** from project root: `PYTHONPATH=Python python Python/run.py` — or from `Python/`: `python run.py`
- **Production:** use a WSGI server (e.g. Gunicorn) pointing at `app:create_app()`

## Imports

Code assumes the **Python** directory is on the import path. Imports look like:

- `from Controller.user_controller import user_bp`
- `from config.db import db`
- `from services.admin_service import AdminService`
- `from repo.user_repo import UserRepo`
- `from utils.crypto_utils import CryptoUtils`

Tests in `tests/` run with `PYTHONPATH=Python` (or equivalent) so these same imports resolve.
