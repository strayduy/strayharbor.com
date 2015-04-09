# Standard libs
import os

class Config(object):
    DEBUG = False

    SECRET_KEY = os.getenv('SECRET_KEY', 'secret_key')
    REDDIT_USERNAME = os.getenv('REDDIT_USERNAME', '')

class ProdConfig(Config):
    USER_DB_HOST = os.getenv('USER_DB_HOST', '')
    USER_DB_NAME = os.getenv('USER_DB_NAME', '')
    USER_DB_USER = os.getenv('USER_DB_USER', '')
    USER_DB_PASSWORD = os.getenv('USER_DB_PASSWORD', '')

class DevConfig(Config):
    DEBUG = True

    USER_DB_HOST = os.getenv('USER_DB_HOST', 'localhost:27017')
    USER_DB_NAME = os.getenv('USER_DB_NAME', '')
    USER_DB_USER = os.getenv('USER_DB_USER', '')
    USER_DB_PASSWORD = os.getenv('USER_DB_PASSWORD', '')

