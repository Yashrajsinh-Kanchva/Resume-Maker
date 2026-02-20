"""
Resume Maker Flask Application Factory

This module creates and configures the Flask application instance with all
necessary blueprints, middleware, and configurations. It follows the application
factory pattern for better testability and modularity.

Key responsibilities:
- Load environment variables
- Initialize Flask app with configuration
- Register all API blueprints
- Configure CORS, sessions, and security settings
- Initialize external services (Redis, Mail, OAuth)
"""

from dotenv import load_dotenv
import os
import logging

from flask import Flask
from flask_cors import CORS

from config.app_config import Config, FSD_DIR
from config.redis_config import redis_client
from Controller.user_controller import user_bp
from Controller.chat_controller import chat_api
from Controller.google_controller import google_bp, init_oauth
from Controller.page_controller import page_bp
from Controller.contact_email_controller import contact_api
from Controller.forgot_password_controller import forgot_password_bp
from Controller.reset_password_controller import reset_password_bp
from Controller.resume_controller import resume_bp
from Controller.feedback_controller import feedback_bp
from Controller.admin_controller import admin_bp
from Controller.admin_data_controller import admin_data_bp
from Controller.admin_analytics_controller import admin_analytics_bp
from Controller.admin_user_action_controller import admin_user_action_bp
from Controller.ai_resume_controller import ai_resume_bp
from Controller.skill_controller import skill_bp
from Controller.ats_controller import ats_bp
from api.admin.chatbot import chatbot_bp

# Load environment variables before importing Config
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)

ADMIN_API_PREFIX = "/api/admin"


def create_app(config_class=Config):
    """
    Application factory function that creates and configures the Flask app.
    
    Args:
        config_class: Configuration class to use (default: Config)
        
    Returns:
        Flask: Configured Flask application instance
        
    Raises:
        RuntimeError: If required environment variables are missing
    """
    # Initialize Flask app
    # NOSONAR
    app = Flask(
        __name__,
        static_folder=FSD_DIR,
        static_url_path=""
    )

    # Load configuration
    app.config.from_object(config_class)

    # Validate required environment variables
    _validate_required_config(app)

    # Configure session security
    _configure_session_security(app)

    # Configure CORS for API endpoints
    _configure_cors(app)

    # Configure email settings
    _configure_mail(app)

    # Initialize external services
    _initialize_services(app)

    # Register all blueprints
    _register_blueprints(app)

    logger.info("Flask application initialized successfully")
    return app


def _validate_required_config(app):
    """
    Validate that all required configuration values are present.
    Only SECRET_KEY is required for startup. Google OAuth is optional (login disabled if missing).
    """
    if not app.config.get("SECRET_KEY"):
        logger.error("SECRET_KEY missing in .env")
        raise RuntimeError("SECRET_KEY missing in .env")

    app.secret_key = app.config["SECRET_KEY"]

    if not app.config.get("GOOGLE_CLIENT_ID") or not app.config.get("GOOGLE_CLIENT_SECRET"):
        logger.warning(
            "GOOGLE_CLIENT_ID or GOOGLE_CLIENT_SECRET missing in .env. Google login will be disabled."
        )


def _configure_session_security(app):
    """
    Configure session cookie security settings.
    
    Args:
        app: Flask application instance
    """
    # Determine if running in production (HTTPS)
    is_production = os.getenv("FLASK_ENV") == "production"

    app.config.update(
        SESSION_COOKIE_HTTPONLY=True,  # Prevent JavaScript access
        SESSION_COOKIE_SAMESITE="Lax",  # CSRF protection
        SESSION_COOKIE_SECURE=is_production  # HTTPS only in production
    )


def _configure_cors(app):
    """
    Configure CORS settings for API endpoints.
    
    Args:
        app: Flask application instance
    """
    allowed_origins = [
        "http://127.0.0.1:5000",
        "http://localhost:5000"
    ]

    # Add production origin if specified
    production_origin = os.getenv("CORS_ORIGIN")
    if production_origin:
        allowed_origins.append(production_origin)

    CORS(
        app,
        resources={
            r"/api/*": {
                "origins": allowed_origins
            }
        },
        supports_credentials=True
    )


def _configure_mail(app):
    """
    Configure email settings and initialize mail service.
    
    Args:
        app: Flask application instance
    """
    app.config.update(
        MAIL_SERVER=os.getenv("MAIL_SERVER", "smtp.gmail.com"),
        MAIL_PORT=int(os.getenv("MAIL_PORT", 587)),
        MAIL_USE_TLS=os.getenv("MAIL_USE_TLS", "True").lower() == "true",
        MAIL_USERNAME=os.getenv("EMAIL_USER"),
        MAIL_PASSWORD=os.getenv("EMAIL_PASS")
    )

    # Initialize mail service
    from utils.mail_utils import init_mail
    init_mail(app)


def _initialize_services(app):
    """
    Initialize external services (Redis, OAuth).
    
    Args:
        app: Flask application instance
    """
    # Initialize Google OAuth
    init_oauth(app)

    # Check Redis connection
    try:
        redis_client.ping()
        logger.info("Redis connection established")
    except Exception as e:
        logger.warning(f"Redis unavailable: {e}")


def _register_blueprints(app):
    """
    Register all Flask blueprints with the application.
    
    Args:
        app: Flask application instance
    """
    # Page routes (static HTML pages)
    app.register_blueprint(page_bp)

    # User authentication and management
    app.register_blueprint(user_bp, url_prefix="/api/users")
    app.register_blueprint(google_bp)  # /api/auth/*

    # Password management
    app.register_blueprint(forgot_password_bp)
    app.register_blueprint(reset_password_bp)

    # Resume management
    app.register_blueprint(resume_bp, url_prefix="/api/resumes")
    app.register_blueprint(ai_resume_bp)
    app.register_blueprint(skill_bp, url_prefix="/api/skills")
    app.register_blueprint(ats_bp)  # /api/ats/*

    # Communication
    app.register_blueprint(chat_api, url_prefix="/api/chat")
    app.register_blueprint(contact_api)
    app.register_blueprint(feedback_bp)

    # Admin endpoints
    app.register_blueprint(admin_bp, url_prefix=ADMIN_API_PREFIX)
    app.register_blueprint(admin_data_bp, url_prefix=ADMIN_API_PREFIX)
    app.register_blueprint(admin_analytics_bp, url_prefix=ADMIN_API_PREFIX)
    app.register_blueprint(admin_user_action_bp, url_prefix=ADMIN_API_PREFIX)
    app.register_blueprint(chatbot_bp, url_prefix=ADMIN_API_PREFIX)
