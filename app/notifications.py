"""Email notifications for the app."""
import datetime as dt
import logging
import smtplib
from email.message import EmailMessage

from fastapi import Depends

from app import config
from app.config import Settings

logger = logging.getLogger(__name__)


def db_created(settings: Settings = Depends(config.get_settings)) -> None:
    """Send an email to the user when a new database is created."""
    yield  # Notification send if database is created
    with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as smtp:
        logger.info("Sending 'db_created' notification")
        timestamp = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug("constructing email message")
        message = EmailMessage()
        message["Subject"] = f"DB Created: {timestamp}"
        message["From"] = settings.notifications_sender
        message["To"] = settings.notifications_target
        message.set_content(f"DB Created: {timestamp}")
        logger.debug("send email result: %s", message)
        smtp.send_message(message)


def db_updated(settings: Settings = Depends(config.get_settings)) -> None:
    """Send an email to the user when a new database is updated."""
    yield  # Notification send if database is updated
    with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as smtp:
        logger.info("Sending 'db_updated' notification")
        timestamp = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug("constructing email message")
        message = EmailMessage()
        message["Subject"] = f"DB Updated: {timestamp}"
        message["From"] = settings.notifications_sender
        message["To"] = settings.notifications_target
        message.set_content(f"DB Updated: {timestamp}")
        logger.debug("send email result: %s", message)
        smtp.send_message(message)
