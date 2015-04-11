# Standard libs
from collections import defaultdict
from datetime import datetime
from dateutil import tz
import math

# Our libs
from .database import Database

# Constants
LOCAL_TIMEZONE = 'America/Los_Angeles'

class MongoDocument(object):
    database = Database
    COLLECTION = ''

    @classmethod
    def get_by_id(cls, _id):
        if not cls.COLLECTION:
            raise NotImplementedError('COLLECTION not set')

        instance = None
        data = cls.database.db[cls.COLLECTION].find_one({'_id': _id})

        if data:
            instance = cls(data)

        return instance

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
    DATE_FORMAT = '%Y-%m-%d'
    DEFAULT_ENTRIES_LIMIT = 25

    def get_likes(self, offset=0, limit=DEFAULT_ENTRIES_LIMIT):
        likes_by_date = defaultdict(list)

        for like in self.get('likes', []):
            utc_date = datetime.utcfromtimestamp(like['created_utc'])
            local_date = convert_utc_to_local(utc_date)
            local_date = local_date.strftime(self.__class__.DATE_FORMAT)

            likes_by_date[local_date].append(like)

        date_entries = sorted([{'date': local_date, 'likes': likes}
                               for local_date, likes
                               in likes_by_date.iteritems()],
                              key=lambda entry: entry['date'],
                              reverse=True)

        paginated_date_entries = self.__class__.paginate_date_entries(date_entries,
                                                                      offset,
                                                                      limit)

        max_pages = int(math.ceil(len(self.get('likes', [])) / float(limit)))

        return {'date_entries': paginated_date_entries, 'max_pages': max_pages}

    @staticmethod
    def paginate_date_entries(date_entries, offset, limit):
        paginated_date_entries = []
        like_index = 0
        max_index = offset + limit - 1

        for date_entry in date_entries:
            paginated_likes = []
            for like in date_entry['likes']:
                if like_index > max_index:
                    break
                if like_index >= offset:
                    paginated_likes.append(like)
                like_index += 1

            if paginated_likes:
                date_entry['likes'] = paginated_likes
                paginated_date_entries.append(date_entry)

            if like_index > max_index:
                break

        return paginated_date_entries

def convert_utc_to_local(utc_date):
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz(LOCAL_TIMEZONE)
    return utc_date.replace(tzinfo=from_zone).astimezone(to_zone)

