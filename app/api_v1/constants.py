from enum import Enum


# Cookiecutter form field types
class FieldType(str, Enum):
    TEXT = "text"
    CHECKBOX = "checkbox"
    SELECT = "select"


# Status codes for 400 errors
class Status401(int, Enum):
    VALUE = 401


class Status403(int, Enum):
    VALUE = 403


class Status404(int, Enum):
    VALUE = 404


class Status422(int, Enum):
    VALUE = 422


# Status codes for 500 errors
class Status500(int, Enum):
    VALUE = 500


class Status501(int, Enum):
    VALUE = 501
