from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "your_project_name"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "your_database_name"
    SECRET_KEY: str = "supersecretkey"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"


settings = Settings()
