from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Tradex"

    class Config:
        env_file = ".env"


settings = Settings()
