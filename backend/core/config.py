from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    app_name: str = "Tradex"
    database_url: str = "sqlite:///./sql_app.db"


settings = Settings()
