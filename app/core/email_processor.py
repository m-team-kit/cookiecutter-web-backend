import datetime as dt
import logging
from pathlib import Path
from typing import Any

import emails
import jinja2
from fastapi import FastAPI

from app.config import Settings


def init_app(app: FastAPI) -> None:
    """Initialize security configuration."""
    settings: Settings = app.state.settings
    app.state.emails = EmailProcessor(settings)


class EmailProcessor:
    def __init__(self, settings: Settings) -> None:
        self.templates_dir = Path(__file__).parent.parent / "email-templates"
        self.logger = logging.getLogger(self.__class__.__name__)
        self._settings = settings

    @property
    def enabled(self) -> bool:
        """Return True if emails are enabled."""
        return self._settings.email_enabled

    @property
    def smtp_options(self) -> dict[str, Any]:
        """Return SMTP options."""
        smtp_options = {"host": self._settings.SMTP_HOST, "port": self._settings.SMTP_PORT}
        if self._settings.SMTP_TLS:
            smtp_options["tls"] = True
        if self._settings.SMTP_USER:
            smtp_options["user"] = self._settings.SMTP_USER
        if self._settings.SMTP_PASSWORD:
            smtp_options["password"] = self._settings.SMTP_PASSWORD
        return smtp_options

    @property
    def from_address(self):
        """Return the from address."""
        return f"{self._settings.email_from_name} <{self._settings.email_from_email}>"

    def db_created(self, email_to: str, environment: dict | None = None) -> None:
        """Send an email to the user when a new database is created."""
        if not self.enabled:
            self.logger.warning("Emails are not enabled. Skipping sending email to %s", email_to)
            return None
        timestamp = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = emails.Message(
            mail_from=self.from_address,
            subject=f"DB Created: {timestamp}",
            html=self.render_template("db_created.j2", timestamp=timestamp),
        )
        response = message.send(to=email_to, render=environment, smtp=self.smtp_options)
        self.logger.info("send email result: %s", response)
        return None

    def db_updated(self, email_to: str, environment: dict | None = None) -> None:
        """Send an email to the user when a new database is updated."""
        if not self.enabled:
            self.logger.warning("Emails are not enabled. Skipping sending email to %s", email_to)
            return None
        timestamp = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = emails.Message(
            mail_from=self.from_address,
            subject=f"DB Updated: {timestamp}",
            html=self.render_template("db_update.j2", timestamp=timestamp),
        )
        response = message.send(to=email_to, render=environment, smtp=self.smtp_options)
        self.logger.info("send email result: %s", response)
        return None

    def render_template(self, template, **kwargs):
        """renders a Jinja template into HTML"""
        templateLoader = jinja2.FileSystemLoader(searchpath="/")
        templateEnv = jinja2.Environment(loader=templateLoader)
        templ = templateEnv.get_template(self.templates_dir / template)
        return templ.render(**kwargs)
