# pylint: disable=missing-module-docstring
from typing import Any, Dict, List, Optional, Set, Union

from pydantic import AnyHttpUrl, EmailStr, HttpUrl, PostgresDsn, validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings, case_sensitive=False):
    # pylint: disable=missing-class-docstring,missing-function-docstring
    # pylint: disable=too-few-public-methods,unused-argument

    project_name: str
    favicon_path: str = "favicon.ico"
    repository_url: AnyHttpUrl

    # `cors_origins` is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    cors_origins: List[AnyHttpUrl] = []

    @validator("cors_origins", pre=True)
    @classmethod
    def assemble_cors_origins(cls, value: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(value, str) and not value.startswith("["):
            return [i.strip() for i in value.split(",")]
        if isinstance(value, (list, str)):
            return value
        raise ValueError(value)

    sentry_dsn: Optional[HttpUrl] = None

    @validator("sentry_dsn", pre=True)
    @classmethod
    def sentry_dsn_can_be_blank(cls, value: str) -> Optional[str]:
        if value is None or len(value) == 0:
            return None
        return value

    # List of trusted OpenID Connect providers
    trusted_op: Set[HttpUrl] = set(["https://aai.egi.eu/auth/realms/egi"])

    # API secret key to operate database
    secret: str

    @validator("secret", pre=True)
    @classmethod
    def secret_quality(cls, value: str) -> str:
        if len(value) < 12:
            raise ValueError(value, "secret must be at least 12 characters long")
        return value

    postgres_host: str
    postgres_user: str
    postgres_password: str
    postgres_db: str = "application"
    postgres_port: int = 5432
    postgres_uri: Optional[PostgresDsn] = None

    @validator("postgres_uri", pre=True)
    @classmethod
    def assemble_db_connection(cls, value: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(value, str):
            return value
        password = values.get("postgres_password")
        user = values.get("postgres_user")
        host = values.get("postgres_host")
        port = values.get("postgres_port")
        path = values.get("postgres_db")
        return f"postgresql://{user}:{password}@{host}:{port}/{path}"

    smtp_tls: bool = True
    smtp_port: Optional[int] = None
    smtp_host: Optional[str] = None
    smtp_user: Optional[str] = None
    smtp_password: Optional[str] = None

    email_from_email: Optional[EmailStr] = None
    email_from_name: Optional[str] = None

    @validator("email_from_name")
    @classmethod
    def get_project_name(cls, value: Optional[str], values: Dict[str, Any]) -> str:
        if not value:
            return values["project_name"]
        return value

    email_reset_token_expire_hours: int = 48
    email_templates_dir: str = "/app/email-templates/build"
    email_enabled: bool = False

    @validator("email_enabled", pre=True)
    @classmethod
    def get_emails_enabled(cls, value: bool, values: Dict[str, Any]) -> bool:
        return bool(values.get("smtp_host") and values.get("smtp_port") and values.get("emails_from_email"))
