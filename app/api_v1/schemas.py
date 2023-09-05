# pylint: disable=too-few-public-methods,missing-module-docstring,missing-class-docstring,redefined-builtin
from typing import Annotated, Optional
from uuid import UUID

from pydantic import BaseModel
from pydantic.functional_validators import AfterValidator
from typing_extensions import TypeAliasType

from app.api_v1 import constants


class Template(BaseModel, from_attributes=True):
    id: UUID
    repoFile: str
    title: str
    summary: str
    language: str
    tags: set[str]
    picture: str
    gitLink: str
    gitCheckout: str
    score: float | None


Templates = TypeAliasType("Templates", list[Template])


class CutterOption(BaseModel, from_attributes=True):
    name: str
    prompt: Optional[str] = None


class CutterField(BaseModel, from_attributes=True):
    type: constants.FieldType
    name: str
    default: str | bool
    options: Optional[list[CutterOption]] = None
    prompt: Optional[str] = None


# CutterForm = TypeAliasType("CutterForm", list[CutterField])
CutterForm = list[CutterField]


class ErrorDetails(BaseModel, from_attributes=True):
    loc: list[str]
    msg: str
    type: str


class Unauthorized(BaseModel, from_attributes=True):
    status_code: constants.Status401 = 401
    detail: list[ErrorDetails]


class Forbidden(BaseModel, from_attributes=True):
    status_code: constants.Status403 = 403
    detail: list[ErrorDetails]


class NotFound(BaseModel, from_attributes=True):
    status_code: constants.Status404 = 404
    detail: list[ErrorDetails]


class Unprocessable(BaseModel, from_attributes=True):
    status_code: constants.Status422 = 422
    detail: list[ErrorDetails]


class ServerError(BaseModel, from_attributes=True):
    status_code: constants.Status500 = 500
    detail: list[ErrorDetails]


class NotImplemented(BaseModel, from_attributes=True):
    status_code: constants.Status501 = 501
    detail: list[ErrorDetails]


def validate_sort_by_field(option, field):
    """Validate sort by field."""
    if option not in ("+", "-"):
        raise ValueError(f"Invalid sort by option '{option}'.")
    if field not in ("id", "score", "title", "language"):
        raise ValueError(f"Invalid sort by field '{field}'.")
    return (option, field)


def validate_sort_by(value: str) -> str:
    """Validate sort by string."""
    for item in value.split(","):
        validate_sort_by_field(item[0], item[1:])
    return value


SortBy = TypeAliasType("SortBy", Annotated[str, AfterValidator(validate_sort_by)])


# class SortBy(str):
#     @classmethod
#     def __get_validators__(cls):
#         yield validate_sort_by


# # To replace fixed Generic once Pydantic supports TypeVarTuple
# SortFields = TypeVarTuple("SortFields")
