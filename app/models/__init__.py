"""Models module to export the models used in the app module. This package contains
the modules to define the models to be used for the app module.
"""

# pylint: disable=missing-module-docstring
from .template import Template, Tag, Score, TagAssociation
from .user import User

__all__ = ["Template", "Tag", "Score", "TagAssociation", "User"]
