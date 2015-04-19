# Standard libs
from collections import OrderedDict
import math

# Third party libs
from flask import abort
from flask import Blueprint
from flask import current_app
from flask import jsonify
from flask import render_template
from flask import request
from repoze.lru import ExpiringLRUCache

# Our libs
from ..models import DATE_FORMAT
from ..models import Like
from ..models import Post
from ..models import User

# Constants
ENTRIES_PER_PAGE = 25
MAX_CACHE_ENTRIES = 50
CACHE_TIMEOUT_IN_SECONDS = 3600 # 1 hour

# Initialize blueprint
blueprint = Blueprint('root', __name__)

# Initialize LRU cache
cache = ExpiringLRUCache(MAX_CACHE_ENTRIES, default_timeout=CACHE_TIMEOUT_IN_SECONDS)

@blueprint.route('/')
@blueprint.route('/page/<int:page>/')
def index(page=1):
    return render_template('index.html')

@blueprint.route('/r/<subreddit>/')
@blueprint.route('/r/<subreddit>/page/<int:page>/')
def subreddit(subreddit, page=1):
    return render_template('subreddit.html', subreddit=subreddit)

@blueprint.route('/posts/')
@blueprint.route('/posts/page/<int:page>/')
def posts(page=1):
    return render_template('posts.html')

@blueprint.route('/posts/<int:year>/<int:month>/<int:day>/<slug>')
def post(year, month, day, slug):
    return render_template('post.html')

@blueprint.route('/posts/<int:year>/<int:month>/<int:day>/<slug>.json')
def post_json(year, month, day, slug):
    post = Post.from_date_slug(year, month, day, slug)
    res = {'post': post.serialize()}
    return jsonify(**res)

@blueprint.route('/date-entries.json')
def likes_json():
    only_posts = request.args.get('only_posts', '').lower() == 'true'
    subreddit = request.args.get('subreddit', '')
    page = int(request.args.get('page', 1))

    cache_key = (only_posts, subreddit, page)
    cache_entry = cache.get(cache_key)

    if cache_entry:
        res = cache_entry
    else:
        posts = [] if subreddit else [p for p in Post.get_all()]
        user = User.get_by_id(current_app.config['REDDIT_USERNAME'])
        likes = [] if only_posts else [l for l in user.get_likes(subreddit=subreddit)]
        offset = ENTRIES_PER_PAGE * (page - 1)

        date_entries = group_posts_and_likes_by_date(posts, likes, offset=offset)

        # Compute max pages
        num_items = len(posts) + len(likes)
        max_pages = int(math.ceil(num_items / float(ENTRIES_PER_PAGE)))

        res = {
            'date_entries': date_entries,
            'max_pages': max_pages
        }

        cache.put(cache_key, res)

    return jsonify(**res)

def group_posts_and_likes_by_date(likes, posts, offset=0, limit=ENTRIES_PER_PAGE):
    date_entries = OrderedDict()
    combined = sorted(posts + likes, key=lambda x: x.date, reverse=True)

    for obj in combined[offset:offset + limit]:
        if isinstance(obj, Post):
            type_key = 'posts'
        elif isinstance(obj, Like):
            type_key = 'likes'
        else:
            continue

        date_str = obj.date.strftime(DATE_FORMAT)
        date_entry = date_entries.setdefault(date_str, {'date': date_str})
        date_entry.setdefault(type_key, []).append(obj.serialize())

    return date_entries.values()

