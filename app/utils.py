"""Utility functions for the app."""
import logging
import tempfile
from typing import Generator

logger = logging.getLogger(__name__)


async def temp_folder() -> Generator:
    """Asynchronous generator to create a temporary folder."""
    logger.debug("Creating temporary folder.")
    with tempfile.TemporaryDirectory() as tempdir:
        yield tempdir
        logger.debug("Removing temporary folder.")


def calculate_score(scores):
    """Calculate the score of a template."""
    logger.debug("Calculating score average for: %s.", scores)
    if not scores:
        return None
    return sum(score.value for score in scores) / len(scores)


def parse_fields(fields_data):
    """Parse fields data into a CutterForm."""
    logger.debug("Collect prompts from fields data.")
    prompts = fields_data.get("__prompts__", {})
    logger.debug("Extract private fields from fields data.")
    data = {k: v for k, v in fields_data.items() if not k.startswith("_")}
    logger.debug("Parse fields data into CutterForm.")
    for name, value in data.items():
        data[name] = parse_field(name, value, prompts.get(name, None))
    logger.debug("Return parsed fields data.")
    return list(data.values())


def parse_field(name, value, prompt=None) -> dict:
    """Parse field data into a CutterField."""
    logger.debug("Parse field='%s' with value='%s' and prompt='%s'.", name, value, prompt)
    if isinstance(value, str):
        data = {"type": "text", "name": name, "default": value}
        data["prompt"] = prompt
        return data
    if isinstance(value, bool):
        data = {"type": "checkbox", "name": name, "default": value}
        data["prompt"] = prompt
        return data
    if isinstance(value, list):
        data = {"type": "select", "name": name, "default": value[0]}
        data["options"] = [{"name": v} for v in value]
        data["prompt"] = prompt.get("__prompt__", None) if prompt else None
        for option in data["options"]:
            option["prompt"] = prompt.get(option["name"], None)
        return data
    raise NotImplementedError(f"Field type '{type(value)}' not supported.")


def validate_sort_by_field(option, field):
    """Validate sort by field."""
    if option not in ("+", "-"):
        raise ValueError(f"Invalid sort by option '{option}'.")
    if field not in ("id", "score", "title"):
        raise ValueError(f"Invalid sort by field '{field}'.")
    return (option, field)


def validate_sort_by(value: str) -> str:
    """Validate sort by string."""
    for item in value.split(","):
        validate_sort_by_field(item[0], item[1:])
    return value


def validate_input(value: str) -> str:
    """Sanitize input string."""
    if "{" in value or "}" in value or "%" in value or "#" in value:
        raise ValueError("Input contains unsafe characters.")
    return value


def unique(session, cls, hashfunc, queryfunc, args, kwds):
    """Get object from database or create it if it does not exist."""
    session.unique_cache = getattr(session, "unique_cache", {})
    key = (cls, hashfunc(*args, **kwds))
    if key in session.unique_cache:
        return session.unique_cache[key]
    else:
        with session.no_autoflush:
            obj = queryfunc(session.query(cls), *args, **kwds).first()
            if not obj:
                obj = cls(*args, **kwds)
                session.add(obj)
        session.unique_cache[key] = obj
        return obj
