"""
Application Entry Point

This module serves as the entry point for running the Flask application
in development mode. For production, use a WSGI server like Gunicorn.

Usage:
    python run.py
"""

import os
from app import create_app

app = create_app()

if __name__ == "__main__":
    # Development server configuration
    # In production, use a proper WSGI server (e.g., Gunicorn)
    app.run(
        host=os.getenv("FLASK_HOST", "0.0.0.0"),
        port=int(os.getenv("FLASK_PORT", 5000)),
        debug=os.getenv("FLASK_DEBUG", "False").lower() == "true"
    )
