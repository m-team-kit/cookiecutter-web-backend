from unittest.mock import patch, MagicMock
import pytest


@pytest.fixture(scope="module")
def patch_session_get_error(app):
    """Mocks the session.get method to raise an exception."""
    with patch.object(app.state, "SessionLocal", MagicMock()) as mock:
        mock.return_value.query = MagicMock(side_effect=Exception("Mocked error"))
        mock.return_value.get = MagicMock(side_effect=Exception("Mocked error"))
        yield
