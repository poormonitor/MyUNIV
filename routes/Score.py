from flask import Blueprint, redirect, render_template, session, request, url_for
from func import login_required, valid_csrf
from const import majors
from models import db
from models.Rank import Rank
import os

score_bp = Blueprint('Score', __name__)


@score_bp.route('/score', methods=['POST'])
@login_required
def score():
    year = int(request.form["exyear"])
    score = int(request.form["score"])
    rank = Rank.query.filter_by(year=year).filter(Rank.rank != 0).order_by(
        db.func.abs(Rank.score - score).asc()).first()
    rank = str(rank.rank) if rank else "0"
    return rank, 200
