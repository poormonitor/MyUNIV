from flask import Blueprint, redirect, render_template, session, request, url_for
from func import login_required, valid_csrf
from const import majors
from models import db
from models.Rank import Rank
import os

score_bp = Blueprint('Score', __name__)


@score_bp.route('/score', methods=['POST'])
@login_required
def modify():
    year = int(request.form["exyear"])
    score = int(request.form["rank"])
    rank = Rank.query.filter_by(Rank.year == year).order_by(
        db.func.abs(Rank.score - score).asc()).first().rank
    return rank, 200
