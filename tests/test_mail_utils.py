"""Tests for utils.mail_utils."""
import pytest
from unittest.mock import MagicMock, patch
from utils import mail_utils


class TestMailUtils:
    @patch("utils.mail_utils.mail")
    def test_init_mail(self, mock_mail):
        app = MagicMock()
        mail_utils.init_mail(app)
        mock_mail.init_app.assert_called_once_with(app)
