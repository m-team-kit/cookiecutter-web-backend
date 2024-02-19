"""Constants for the API."""

# pylint: disable=too-few-public-methods,missing-module-docstring,missing-class-docstring
from enum import Enum


# Cookiecutter form field types
class FieldType(str, Enum):
    """Constants for the form field types."""

    TEXT = "text"
    CHECKBOX = "checkbox"
    SELECT = "select"


# Status codes for 400 errors
class Status401(int, Enum):
    """Constant for the status code 401."""

    VALUE = 401


class Status403(int, Enum):
    """Constant for the status code 403."""

    VALUE = 403


class Status404(int, Enum):
    """Constant for the status code 404."""

    VALUE = 404


class Status422(int, Enum):
    """Constant for the status code 422."""

    VALUE = 422


# Status codes for 500 errors
class Status500(int, Enum):
    """Constant for the status code 500."""

    VALUE = 500


class Status501(int, Enum):
    """Constant for the status code 501."""

    VALUE = 501
