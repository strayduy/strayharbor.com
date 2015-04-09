#!python2.7

# Third party libs
from flask.ext.script import Manager

# Our libs
from strayharbor.app import create_app
from strayharbor.settings import DevConfig

def main():
    app = create_app(DevConfig)
    manager = Manager(app)
    manager.run()

if __name__ == '__main__':
    main()

