"""Tests for Controller.skill_controller."""
import pytest
from unittest.mock import patch


@patch("Controller.skill_controller.suggest_skills")
def test_skill_suggest_returns_json(mock_suggest):
    from flask import Flask
    from Controller.skill_controller import skill_bp
    mock_suggest.return_value = ["python", "flask"]
    app = Flask(__name__)
    app.register_blueprint(skill_bp)
    with app.test_client() as client:
        rv = client.get("/suggest?q=py")
        assert rv.status_code == 200
        data = rv.get_json()
        assert data == ["python", "flask"]
    mock_suggest.assert_called_once_with("py")


def test_skill_suggest_empty_q():
    from flask import Flask
    from Controller.skill_controller import skill_bp
    app = Flask(__name__)
    app.register_blueprint(skill_bp)
    with app.test_client() as client:
        rv = client.get("/suggest")
        assert rv.status_code == 200
        data = rv.get_json()
        assert isinstance(data, list)
