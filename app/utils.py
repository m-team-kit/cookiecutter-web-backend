import logging

logger = logging.getLogger(__name__)


def score_calculation(template):
    """Calculate the score of a template."""
    logger.debug("Calculating score of template: %s.", template.repoFile)
    if len(template.scores) == 0:
        logger.debug("Template %s has no scores.", template.repoFile)
        return None
    logger.debug("Template %s has %s scores.", template.repoFile, len(template.scores))
    return sum(score.value for score in template.scores) / len(template.scores)


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
