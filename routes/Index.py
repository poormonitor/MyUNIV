from flask import Blueprint, render_template, session

index_bp = Blueprint('Index', __name__)


@index_bp.route('/')
def index():
    print(session.items())
    return render_template('index.html', session=session)