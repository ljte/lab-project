import os

from pydantic import BaseSettings, Field
from dotenv import load_dotenv


dotenv_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "dev.env"
)
print(dotenv_path)
load_dotenv(dotenv_path)


class Config(BaseSettings):
    SECRET_KEY: str = Field(None, env="SECRET_KEY")
    DATABASE_URI: str = Field(None, env="DATABASE_URI")


class TestConfig(Config):
    DATABASE_URI = "sqlite:///:memory:"
