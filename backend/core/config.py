from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Tradex"
    # When running under Docker the PostgreSQL service is reachable by the
    # container name `db`. This serves as the default connection string but can
    # be overridden via the `DATABASE_URL` environment variable.
    database_url: str = "postgresql://postgres:postgres@db:5432/postgres"
    secret_key: str = "changeme"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
