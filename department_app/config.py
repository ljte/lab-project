"""flask app config"""

import os

from dotenv import load_dotenv


load_dotenv()


class Config:
    """default config"""
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')


class TestConfig(Config):
    """config for tests"""
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DB_URI')
