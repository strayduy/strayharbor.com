#!python2.7

# Standard libs
import argparse
from collections import OrderedDict
import logging
import os
import re
import sys
import time

# Third party libs
import flask
import pymongo
import requests

# Our libs
from ..database import Database
from ..models import User
from ..settings import DevConfig, ProdConfig

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Fetch reddit links that a '
                                                 'given user has liked')
    parser.add_argument('reddit_username')
    args = parser.parse_args()

    # Load config based on environment
    env = os.getenv('APP_ENV', 'prod')
    config = get_config(env)

    # Configure logging
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    # Connect to database
    connect_to_database(config)
    Database.db['upvotes'].remove()

    # Find the user's most recent upvote
    most_recent_upvote = None
    user = User.get_by_id(args.reddit_username)
    if user:
        most_recent_upvote = user.get_most_recent_upvote()

    # Fetch recent upvotes
    redditor = Redditor(args.reddit_username)

    logging.debug('Fetching upvotes for /u/%s' % (redditor.username))
    upvotes = redditor.get_upvotes(since=most_recent_upvote)
    logging.debug('Found %d new upvotes for /u/%s' % (len(upvotes),
                                                      redditor.username))

    # Nothing to store
    if not upvotes:
        return

    # Create a user record if it doesn't already exist
    if not user:
        user_data = {
            '_id': redditor.username,
            'username': redditor.username,
        }
        user = User.create(user_data)

    # Save upvotes
    user.save_upvotes(upvotes)

def get_config(env):
    config = flask.config.Config('')

    if env.lower() == 'prod':
        config.from_object(ProdConfig())
    else:
        config.from_object(DevConfig())

    return config

def connect_to_database(config):
    db_config = {
        'host': config.get('USER_DB_HOST', ''),
        'name': config.get('USER_DB_NAME', ''),
        'user': config.get('USER_DB_USER', ''),
        'password': config.get('USER_DB_PASSWORD', ''),
    }

    Database.connect(**db_config)

class Redditor(object):
    USERNAME_REGEX = re.compile(r'^[\w_-]{3,20}$')
    API_BASE_URL = 'http://www.reddit.com'
    API_USER_AGENT = os.getenv('REDDIT_API_USER_AGENT', '')
    LIKES_PER_PAGE = 100
    MAX_PAGES = 20
    REQUEST_DELAY_IN_SECONDS = 2

    def __init__(self, username):
        if not self.__class__.USERNAME_REGEX.match(username):
            raise Exception('Invalid reddit username')

        self.username = username

        self.api_headers = {}
        self.api_headers['User-Agent'] = self.__class__.API_USER_AGENT

    def get_upvotes(self, since=None):
        cls = self.__class__
        endpoint = '/user/%s/upvoted.json' % (self.username)
        endpoint_url = self.__class__.API_BASE_URL + endpoint

        upvotes = []
        after = None
        found_most_recent_upvote = False

        for page in xrange(cls.MAX_PAGES):
            if page > 0:
                time.sleep(cls.REQUEST_DELAY_IN_SECONDS)

            params = {
                'limit': cls.LIKES_PER_PAGE,
                'sort': 'new',
            }

            if after:
                params['after'] = after

            res = requests.get(endpoint_url,
                               params=params,
                               headers=self.api_headers)
            res_data = res.json()['data']

            for child in res_data['children']:
                upvote = child['data']

                if since and upvote['name'] == since['name']:
                    found_most_recent_upvote = True

                upvotes.append(upvote)

            if found_most_recent_upvote:
                break

            after = res_data['after']
            if not after:
                break

        return upvotes

if __name__ == '__main__':
    main()

