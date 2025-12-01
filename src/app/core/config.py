from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Loads environment variables from .env file.
    """

    DATABASE_URL: str
    LOG_LEVEL: str
    FLASK_API_DATETIME_FORMAT: str = "%G-%m-%dT%H:%M:%S%:z"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()  # type: ignore
