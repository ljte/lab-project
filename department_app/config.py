import os

from pydantic import BaseSettings, Field
from dotenv import load_dotenv


dotenv_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "dev.env")
load_dotenv(dotenv_path)


class Config(BaseSettings):
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    DATABASE_URI: str = Field(..., env="DATABASE_URI")


config = Config()