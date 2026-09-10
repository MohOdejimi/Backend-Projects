from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    mongo_uri: str
    mongo_db_name: str
    secret_key: str
    access_token_expire_minutes: int = 60

    class Config:
        env_file = "./.env"

settings = Settings()