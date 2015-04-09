#!python2.7

# Standard libs
import os

# Our libs
from .app import create_app
from .settings import DevConfig, ProdConfig

env = os.getenv('APP_ENV', 'dev')

if env.lower() == 'prod':
    app = create_app(ProdConfig)
else:
    app = create_app(DevConfig)

