from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite:///./ms_leaders.db"

    class Config:
        env_file = ".env"


settings = Settings()
