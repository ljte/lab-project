"""flask app config"""

import os

from dotenv import load_dotenv


load_dotenv()


class Config:
    """default config"""
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
    SECRET_KEY = os.environ.get('SECRET_KEY')


class TestConfig(Config):
    """config for tests"""
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DB_URI')
    TESTING = True


class LiveServerTest(Config):
    """config fog tests with server"""
    TESTING = True
    LIVESERVER_PORT = 5000
