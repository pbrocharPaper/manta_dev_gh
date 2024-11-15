from pydantic_settings import BaseSettings


# load settings from dotenv file
class Settings(BaseSettings):
    GITHUB_API_KEY: str

    class Config:
        env_file = ".env"


def get_settings():
    return Settings()
