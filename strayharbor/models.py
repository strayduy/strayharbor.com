# Standard libs
from datetime import datetime
from dateutil import tz
import markdown
import os
import re

# Third party libs
import pymongo

# Our libs
from .database import Database

# Constants
LOCAL_TIMEZONE = os.getenv('TZ', 'America/Los_Angeles')
DATE_FORMAT = '%Y-%m-%d'

class MongoDocument(object):
    database = Database
    COLLECTION = ''

    @classmethod
    def create(cls, data):
        if not cls.COLLECTION:
            raise NotImplementedError('COLLECTION not set')

        # Create a shallow copy so we don't mutate the original data
        data_copy = data.copy()
        data_copy['created_on'] = datetime.utcnow()

        _id = cls.database.db[cls.COLLECTION].insert(data_copy)
        instance = cls(data=data_copy)
        instance['_id'] = _id

        return instance

    @classmethod
    def get_by_id(cls, _id):
        if not cls.COLLECTION:
            raise NotImplementedError('COLLECTION not set')

        instance = None
        data = cls.database.db[cls.COLLECTION].find_one({'_id': _id})

        if data:
            instance = cls(data=data)

        return instance

    @classmethod
    def find(cls, query, fields=None, limit=None, sort=None):
        if not cls.COLLECTION:
            raise NotImplementedError('COLLECTION not set')

        cursor = cls.database.db[cls.COLLECTION].find(query, fields)

        if limit:
            cursor.limit(limit)

        if sort:
            cursor.sort(sort)

        return (cls(document) for document in cursor)

    def __init__(self, data=None):
        self.data = data if data else {}

    def __getitem__(self, name):
        return self.data[name]

    def __setitem__(self, name, value):
        self.data[name] = value

    def get(self, name, default=None):
        return self.data.get(name, default)

class User(MongoDocument):
    COLLECTION = 'users'
    DEFAULT_ENTRIES_LIMIT = 25

    def get_upvotes(self, subreddit=None):
        query = {'username': self['_id']}
        sort = [('created_utc', pymongo.DESCENDING)]

        upvotes = [u for u in Upvote.find(query, sort=sort)]

        for upvote in upvotes:
            if not subreddit or subreddit == upvote['subreddit']:
                yield upvote

    def get_most_recent_upvote(self):
        query = {'username': self['_id']}
        sort = [('created_on', pymongo.DESCENDING)]

        upvotes = [u for u in Upvote.find(query, limit=1, sort=sort)]

        return Upvote(data=upvotes[0]) if upvotes else None

    def save_upvotes(self, upvotes):
        for upvote in upvotes:
            try:
                # Create a copy to avoid mutating the original
                upvote_copy = upvote.copy()
                upvote_copy['_id'] = upvote_copy['name']
                upvote_copy['username'] = self['_id']

                Upvote.create(data=upvote_copy)
            except pymongo.errors.DuplicateKeyError:
                # We already saved this upvote
                # We're okay with this error, so we can ignore it
                pass

class Upvote(MongoDocument):
    COLLECTION = 'upvotes'
    FIELDS = [
        'created_utc',
        'num_comments',
        'permalink',
        'subreddit',
        'thumbnail',
        'title',
        'url',
    ]

    @property
    def date(self):
        utc_date = datetime.utcfromtimestamp(self['created_utc'])
        local_date = convert_utc_to_local(utc_date)
        return local_date

    def serialize(self):
        serialized = {}

        for field in self.__class__.FIELDS:
            serialized[field] = self[field]

        return serialized

class Post(object):
    POSTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'posts')
    FILENAME_REGEX = re.compile(r'^(\d{4}-\d{2}-\d{2})-(.+)\.md$')

    @classmethod
    def get_all(cls):
        sorted_filepaths = sorted(os.listdir(cls.POSTS_DIR), reverse=True)
        for filepath in sorted_filepaths:
            post = cls.from_filepath(filepath)
            if not post:
                continue

            yield post

    @classmethod
    def from_filepath(cls, filepath):
        match_obj = cls.FILENAME_REGEX.match(filepath)
        if not match_obj:
            return None

        post = Post()

        post.date = datetime.strptime(match_obj.group(1), DATE_FORMAT)

        # Set post date to local timezone
        local_tz = tz.gettz(LOCAL_TIMEZONE)
        post.date = post.date.replace(tzinfo=local_tz).astimezone(local_tz)

        post.slug = match_obj.group(2)
        post.filepath = os.path.join(cls.POSTS_DIR, filepath)
        post._title = ''
        post._content = ''

        return post

    @classmethod
    def from_date_slug(cls, year, month, day, slug):
        filepath = '%04d-%02d-%02d-%s.md' % (year, month, day, slug)
        #filepath = os.path.join(cls.POSTS_DIR, basename)
        return cls.from_filepath(filepath)

    def __init__(self):
        self.has_loaded_file = False

    def load_file(self):
        with open(self.filepath, 'r') as f:
            self._title = f.readline().strip()
            self._content = ''.join(f.readlines()).strip()

        self.has_loaded_file = True

    @property
    def title(self):
        if not self.has_loaded_file:
            self.load_file()

        return self._title

    @property
    def content(self):
        if not self.has_loaded_file:
            self.load_file()

        return self._content

    @property
    def url(self):
        return self.date.strftime('/posts/%Y/%m/%d/') + self.slug

    def serialize(self):
        serialized = {
            'date': self.date.strftime(DATE_FORMAT),
            'slug': self.slug,
            'title': self.title,
            'content': markdown.markdown(self.content),
            'url': self.url,
        }

        return serialized

def convert_utc_to_local(utc_date):
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz(LOCAL_TIMEZONE)
    return utc_date.replace(tzinfo=from_zone).astimezone(to_zone)

