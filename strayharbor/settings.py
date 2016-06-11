# Standard libs
import os

class Config(object):
    DEBUG = False

    SECRET_KEY = os.getenv('SECRET_KEY', 'secret_key')
    REDDIT_USERNAME = os.getenv('REDDIT_USERNAME', '')

class ProdConfig(Config):
    APP_ENV = 'prod'

    USER_DB_HOST = os.getenv('USER_DB_HOST', '')
    USER_DB_NAME = os.getenv('USER_DB_NAME', '')
    USER_DB_USER = os.getenv('USER_DB_USER', '')
    USER_DB_PASSWORD = os.getenv('USER_DB_PASSWORD', '')

    MINIFY_PAGE = True

class DevConfig(Config):
    APP_ENV = 'dev'

    DEBUG = True

    USER_DB_HOST = os.getenv('USER_DB_HOST', 'localhost:27017')
    USER_DB_NAME = os.getenv('USER_DB_NAME', '')
    USER_DB_USER = os.getenv('USER_DB_USER', '')
    USER_DB_PASSWORD = os.getenv('USER_DB_PASSWORD', '')

    WEBPACK_DEV_SERVER_HOSTNAME = os.getenv('WEBPACK_DEV_SERVER_HOSTNAME', 'localhost:8080')

