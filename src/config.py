from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    POSTGRES_USER: str = Field(...)
    POSTGRES_PASSWORD: str = Field(...)
    POSTGRES_DB: str = Field(...)
    MAX_ATTEMPTS: int = Field(
        ...
    )  # Specifies the max amount of server attempts to retrieve at least one question

    @property
    def POSTGRES_URL(self) -> str:
        return f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@db:5432/{self.POSTGRES_DB}"


config = Config(_env_file=".env", _env_file_encoding="utf-8")
