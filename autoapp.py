"""Create an application instance."""
import logging

from fastapi import FastAPI

from alembic import command
from alembic.config import Config
from app import create_app

app: FastAPI = create_app()
logging.info("Running DB migrations")
alembic_cfg = Config("alembic.ini")
command.upgrade(alembic_cfg, "head")
