from flask import Blueprint, render_template, session

index_bp = Blueprint('Index', __name__)


@index_bp.route('/')
def index():
    return render_template('index.html', session=session)