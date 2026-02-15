from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite:///./ms_projects.db"
    leaders_service_url: str = "http://127.0.0.1:8001"

    class Config:
        env_file = ".env"


settings = Settings()
