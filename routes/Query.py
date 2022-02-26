from models.Major import Major
from flask import Blueprint, render_template, request, abort, session, redirect

query_bp = Blueprint('Query', __name__)

@query_bp.route('/query', methods=['GET'])
def query():
    if request.method == 'GET':
        return render_template('query.html')
