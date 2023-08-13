from flask import Blueprint, request
from models import db
from models.Rank import Rank

score_bp = Blueprint("Score", __name__)


@score_bp.route("/score", methods=["POST"])
def score():
    year = int(request.form["exyear"])
    score = int(request.form["score"])
    rank = (
        Rank.query.filter_by(year=year)
        .filter(Rank.rank != 0)
        .order_by(db.func.abs(Rank.score - score).asc())
        .order_by(Rank.rank.desc())
        .first()
    )
    if not rank:
        rank = "0"
    elif rank.score != score:
        s_rank = (
            Rank.query.filter_by(year=year)
            .filter(Rank.rank != 0)
            .order_by(Rank.rank.asc(), db.func.abs(Rank.score - score).desc())
            .first()
        )
        rank = str((rank.rank + s_rank.rank) // 2) if s_rank else str(rank.rank)
    else:
        rank = str(rank.rank)
    return rank, 200
