from fastapi import FastAPI
from flaat.fastapi import Flaat

from app.config import Settings


def init_app(app: FastAPI) -> None:
    """Initialize security configuration."""
    settings: Settings = app.state.settings
    app.state.flaat = Flaat()
    op_list = [str(x) for x in settings.trusted_op]
    app.state.flaat.set_trusted_OP_list(op_list)
