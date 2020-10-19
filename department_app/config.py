import os

from dotenv import load_dotenv


load_dotenv()


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DB_URI')
