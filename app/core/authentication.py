from fastapi import FastAPI
from flaat.fastapi import Flaat

from app.config import Settings


def init_app(app: FastAPI, settings: Settings) -> None:
    """Initialize security configuration."""
    app.state.flaat = Flaat()
    app.state.flaat.set_trusted_OP_list([str(x) for x in settings.trusted_op])
