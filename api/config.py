from functools import lru_cache
from dotenv import load_dotenv
from pydantic_settings import BaseSettings


load_dotenv()


@lru_cache()
def settings():
    return Settings()


class Settings(BaseSettings):
    mysql_url: str