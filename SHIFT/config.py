from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    EXPIRE_MINUTES: int

    PG_HOST: str
    PG_PORT: str
    PG_USERNAME: str
    PG_PASSWORD: str
    PG_DATABASE: str

    @property
    def url_asyncpg(self):
        return (f"postgresql+asyncpg://"
                f"{self.PG_USERNAME}:{self.PG_PASSWORD}@{self.PG_HOST}:{self.PG_PORT}/{self.PG_DATABASE}")


base_dir = Path(__file__).resolve().parent.parent
load_dotenv(base_dir / ".env")
config = Config()
