import os

from dotenv import load_dotenv


dotenv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dev.env")
load_dotenv(dotenv_path)


class BasicConfig:
    SECRET_KEY = os.getenv("SECRET_KEY")
    DATABASE_URI = os.getenv("DATABASE_URI")
