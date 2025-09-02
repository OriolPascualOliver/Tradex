from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Tradex"
    database_url: str = "sqlite:///./sql_app.db"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
