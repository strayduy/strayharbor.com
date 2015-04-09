# Third party libs
from flask import abort
from flask import Blueprint
from flask import current_app
from flask import jsonify
from flask import render_template
from flask import request

# Our libs
from ..models import User

# Constants
ENTRIES_PER_PAGE = 25

# Initialize blueprint
blueprint = Blueprint('root', __name__)

@blueprint.route('/')
@blueprint.route('/page/<int:page>/')
def index(page=1):
    return render_template('index.html')

@blueprint.route('/likes.json')
def likes_json():
    page = int(request.args.get('page', 1))
    offset = ENTRIES_PER_PAGE * (page - 1)

    user = User.get_by_id(current_app.config['REDDIT_USERNAME'])
    res = user.get_likes(offset=offset, limit=ENTRIES_PER_PAGE)
    return jsonify(**res)

