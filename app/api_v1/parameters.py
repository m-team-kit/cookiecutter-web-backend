"""Parameters for the API endpoints."""

# pylint: disable=missing-module-docstring
from fastapi import Query, Path

#: Query parameter for the tags filter
tags = Query(
    title="Tags",
    description=" Tags to filter by, return templates should include all tags.",
    default=[],
    json_schema_extra={"type": "array", "items": {"type": "string"}, "example": ["python"]},
)


#: Query parameter for the list of keywords
keywords = Query(
    title="Keywords",
    description="List of keywords (string subsets).",
    default=[],
    json_schema_extra={"type": "array", "items": {"type": "string"}},
)


#: Query parameter for the sort order
sort_by = Query(
    title="Sort by",
    description="Order to return the results (comma separated). Generic fields are ['±id', '±score', '±title'].",
    default="-score",
    json_schema_extra={"type": "string", "example": "+title,-score"},
)


#: Query parameter for the template UUID
template_uuid = Path(
    title="Template UUID",
    description="UUID of the template to be used for generating a new software project.",
)
