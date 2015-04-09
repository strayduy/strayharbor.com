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
import pymongo
import requests

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Fetch reddit links that a '
                                                 'given user has liked')
    parser.add_argument('reddit_username')
    args = parser.parse_args()

    # Configure logging
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    # Initialize database and User model
    db = Database.connect()
    User.db = db

    # Find the user's most recent like
    most_recent_like = None
    user = User.get(args.reddit_username)
    if user:
        most_recent_like = user.get_most_recent_like()

    redditor = Redditor(args.reddit_username)

    logging.debug('Fetching likes for /u/%s' % (redditor.username))
    likes = redditor.get_likes(since=most_recent_like)
    logging.debug('Found %d new likes for /u/%s' % (len(likes),
                                                    redditor.username))

    # Save the user's likes to our database
    if user:
        user.save_likes(likes)
    else:
        User.create(redditor.username, likes)

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

    def get_likes(self, since=None):
        cls = self.__class__
        endpoint = '/user/%s/liked.json' % (self.username)
        endpoint_url = self.__class__.API_BASE_URL + endpoint

        likes = []
        after = None
        found_most_recent_like = False

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
                like = child['data']

                if since and like['name'] == since['name']:
                    found_most_recent_like = True
                    break

                likes.append(like)

            if found_most_recent_like:
                break

            after = res_data['after']
            if not after:
                break

        return likes

class User(object):
    db = None

    @classmethod
    def get(cls, username):
        user = None
        collection = cls.db.users
        user_data = collection.find_one({'_id': username})

        if user_data:
            user = User(user_data)

        return user

    @classmethod
    def create(cls, username, likes):
        collection = cls.db.users
        collection.insert({'_id': username, 'likes': likes})

    def __init__(self, data):
        self.username = data['_id']
        self.likes = data.get('likes', [])

    def get_most_recent_like(self):
        return self.likes[0] if self.likes else None

    def save_likes(self, likes):
        # Prepend likes to self.likes
        likes.extend(self.likes)
        self.likes = likes

        # Dedupe list
        # http://stackoverflow.com/a/17016257
        self.likes = list(OrderedDict.fromkeys(self.likes))

        collection = self.__class__.db.users
        collection.update({'_id': self.username},
                          {'$set': {'likes': self.likes}})

class Database(object):
    HOST = os.getenv('USER_DB_HOST', '')
    NAME = os.getenv('USER_DB_NAME', '')
    USER = os.getenv('USER_DB_USER', '')
    PASSWORD = os.getenv('USER_DB_PASSWORD', '')

    @classmethod
    def connect(cls):
        client = pymongo.MongoClient(cls.HOST)
        db = client[cls.NAME]
        db.authenticate(cls.USER, cls.PASSWORD)
        return db

if __name__ == '__main__':
    main()

