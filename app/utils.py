def score_calculation(template):
    """Calculate the score of a template."""
    if len(template.scores) == 0:
        return None
    return sum(score.value for score in template.scores) / len(template.scores)
