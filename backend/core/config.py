from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Tradex"
    database_url: str = "sqlite:///./sql_app.db"
    secret_key: str = "changeme"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
