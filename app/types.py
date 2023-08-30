from typing import Annotated

from pydantic.functional_validators import AfterValidator
from typing_extensions import TypeAliasType


def validate_sort_by_field(option, field):
    """Validate sort by field."""
    if option not in ("+", "-"):
        raise ValueError(f"Invalid sort by option '{option}'.")
    if field not in ("id", "score", "title", "language"):
        raise ValueError(f"Invalid sort by field '{field}'.")
    return (option, field)


def validate_sort_by(v: str) -> str:
    """Validate sort by string."""
    for item in v.split(","):
        validate_sort_by_field(item[0], item[1:])
    return v


SortBy = TypeAliasType("SortBy", Annotated[str, AfterValidator(validate_sort_by)])


# from typing import TypeVarTuple, Generic


# class SortBy(str):
#     @classmethod
#     def __get_validators__(cls):
#         yield validate_sort_by


# # To replace fixed Generic once Pydantic supports TypeVarTuple
# SortFields = TypeVarTuple("SortFields")
