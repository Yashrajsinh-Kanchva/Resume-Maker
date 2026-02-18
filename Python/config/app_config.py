"""
Application Configuration Module

This module defines the Flask application configuration class and provides
path constants for accessing frontend static files (HTML, CSS, JS, images).

The Config class loads sensitive values from environment variables with
appropriate defaults for development.
"""

import os


# Base directory paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
FSD_DIR = os.path.join(BASE_DIR, "FSD")

# Frontend static file directories
HTML_DIR = os.path.join(FSD_DIR, "HTML")
CSS_DIR = os.path.join(FSD_DIR, "CSS")
JS_DIR = os.path.join(FSD_DIR, "JS")
IMG_DIR = os.path.join(FSD_DIR, "IMG")


class Config:
    """
    Flask application configuration class.
    
    Loads configuration values from environment variables. Sensitive values
    like SECRET_KEY and OAuth credentials should be set in .env file.
    
    Attributes:
        SECRET_KEY: Flask secret key for session management
        GOOGLE_CLIENT_ID: Google OAuth client ID
        GOOGLE_CLIENT_SECRET: Google OAuth client secret
        SESSION_COOKIE_HTTPONLY: Prevent JavaScript access to cookies
        SESSION_COOKIE_SAMESITE: CSRF protection setting
    """
    
    # Flask secret key - MUST be set in production
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "dev-secret-key-change-in-production")

    # Google OAuth credentials
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

    # Session security settings
    SESSION_COOKIE_HTTPONLY = True  # Prevent XSS attacks
    SESSION_COOKIE_SAMESITE = "Lax"  # CSRF protection
