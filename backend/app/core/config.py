from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "TalentLens AI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    OPENAI_API_KEY: str = ""
    EMBEDDING_MODEL: str = "BAAI/bge-small-en-v1.5"

    class Config:
        env_file = ".env"


settings = Settings()