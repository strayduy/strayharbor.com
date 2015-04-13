# Third party libs
from flask import abort
from flask import Blueprint
from flask import current_app
from flask import jsonify
from flask import render_template
from flask import request
from repoze.lru import ExpiringLRUCache

# Our libs
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

@blueprint.route('/likes.json')
def likes_json():
    subreddit = request.args.get('subreddit', '')
    page = int(request.args.get('page', 1))

    cache_key = '/likes.json?subreddit=%s&page=%d' % (subreddit, page)
    cache_entry = cache.get(cache_key)

    if cache_entry:
        res = cache_entry
    else:
        offset = ENTRIES_PER_PAGE * (page - 1)
        user = User.get_by_id(current_app.config['REDDIT_USERNAME'])
        res = user.get_likes(offset=offset, limit=ENTRIES_PER_PAGE, subreddit=subreddit)
        cache.put(cache_key, res)

    return jsonify(**res)

