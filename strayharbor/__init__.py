# Third party libs
from flask import Flask

# Our libs
from .blueprints import root
from .database import Database

def create_app(config_object):
    app = Flask(__name__, static_folder='client/static')
    app.config.from_object(config_object)

    register_extensions(app)
    register_blueprints(app)

    return app

def register_extensions(app):
    db_config = {
        'host': app.config.get('USER_DB_HOST', ''),
        'name': app.config.get('USER_DB_NAME', ''),
        'user': app.config.get('USER_DB_USER', ''),
        'password': app.config.get('USER_DB_PASSWORD', ''),
    }
    Database.connect(**db_config)

def register_blueprints(app):
    app.register_blueprint(root.blueprint)

