# pylint: disable=too-few-public-methods,missing-module-docstring,missing-class-docstring,redefined-builtin
from typing import Annotated, Optional
from uuid import UUID

from pydantic import BaseModel, conint
from pydantic.functional_validators import AfterValidator
from typing_extensions import TypeAliasType

from app.api_v1 import constants
from app import utils


Score = TypeAliasType("Score", conint(ge=0, le=5))
SortBy = TypeAliasType("SortBy", Annotated[str, AfterValidator(utils.validate_sort_by)])
Input = TypeAliasType("Input", Annotated[str, AfterValidator(utils.validate_input)])


# class SortBy(str):
#     @classmethod
#     def __get_validators__(cls):
#         yield validate_sort_by


# # To replace fixed Generic once Pydantic supports TypeVarTuple
# SortFields = TypeVarTuple("SortFields")


class Template(BaseModel, from_attributes=True):
    id: UUID
    repoFile: str
    title: str
    summary: str
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
