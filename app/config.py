"""Application module to load configuration."""

# pylint: disable=missing-class-docstring
from typing import Optional, Union

from fastapi import FastAPI, Request
from pydantic import AnyHttpUrl, HttpUrl, PostgresDsn, field_validator, model_validator
from pydantic_settings import BaseSettings
from starlette.middleware.cors import CORSMiddleware


class Settings(BaseSettings, case_sensitive=False):
    """Application settings from BaseSettings by Pydantic.
    This class is used to load the configuration from environment variables.
    """

    # pylint: disable=missing-function-docstring
    # pylint: disable=too-few-public-methods,unused-argument

    project_name: str
    favicon_path: str = "favicon.ico"
    repository_url: AnyHttpUrl

    # `cors_origins` is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    cors_origins: list[AnyHttpUrl] = []

    @field_validator("cors_origins")
    @classmethod
    def assemble_cors_origins(cls, value: Union[str, list[str]]) -> Union[list[str], str]:
        if isinstance(value, str) and not value.startswith("["):
            return [i.strip() for i in value.split(",")]
        return value

    # List of trusted OpenID Connect providers
    trusted_op: set[HttpUrl] = set(["https://aai.egi.eu/auth/realms/egi"])

    # API secret key to operate database
    admin_secret: str

    @field_validator("admin_secret")
    @classmethod
    def secret_quality(cls, value: str) -> str:
        if len(value) < 12:
            raise ValueError(value, "secret must be at least 12 characters long")
        return value

    postgres_host: str = "localhost"
    postgres_db: str = "application"
    postgres_user: str
    postgres_password: str
    postgres_port: int = 5432

    @property
    def postgres_uri(self) -> PostgresDsn:
        password = self.postgres_password
        user = self.postgres_user
        host = self.postgres_host
        port = self.postgres_port
        path = self.postgres_db
        return f"postgresql://{user}:{password}@{host}:{port}/{path}"

    notifications_sender: Optional[str] = None
    notifications_target: Optional[str] = None
    smtp_port: Optional[int] = 587
    smtp_host: Optional[str] = "postfix"

    @model_validator(mode="after")
    def target_requires_sender(self) -> "Settings":
        if self.notifications_target and not self.notifications_sender:
            raise ValueError("notifications_sender is required if notifications_target is set")
        return self


def set_settings(app: FastAPI, **custom_parameters: dict) -> None:
    """Set the settings object on the application."""
    app.state.settings = Settings(**custom_parameters)
    app.title = app.state.settings.project_name
    app.description = __doc__
    app.openapi_url = "/api/openapi.json"
    app.separate_input_output_schemas = False
    set_cors(app, app.state.settings)


def get_settings(request: Request) -> Settings:
    """Return the settings object."""
    return request.app.state.settings


def set_cors(app: FastAPI, settings: Settings) -> None:
    """Set all CORS enabled origins."""
    origins = [str(origin) for origin in settings.cors_origins]
    if origins is not []:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
