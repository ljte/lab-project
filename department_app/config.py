import os

from dotenv import load_dotenv
from pydantic import BaseSettings, Field

dotenv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dev.env")
load_dotenv(dotenv_path)


class Config(BaseSettings):
    SECRET_KEY: str = Field(None, env="SECRET_KEY")
    DATABASE_URI: str = Field(None, env="DATABASE_URI")


class TestConfig:
    DATABASE_URI = "sqlite:///:memory:"
    TESTING = True

    @classmethod
    def dict(cls):
        return cls.__dict__
