from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "SafeRoute+"
    ENV: str = "dev"

    class Config:
        env_file = ".env"

settings = Settings()
