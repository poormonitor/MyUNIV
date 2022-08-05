from flask import Blueprint, render_template, session
from models.Rank import Rank
from models import db
import json

index_bp = Blueprint("Index", __name__)


@index_bp.route("/")
def index():
    totals = (
        db.session.query(Rank.year, db.func.sum(Rank.schedule))
        .group_by(Rank.year)
        .order_by(Rank.year.asc())
        .all()
    )
    totals = [[str(i[0]), i[1]] for i in totals]
    totals = json.dumps(totals)
    notice = session.get("notice", None)
    session["notice"] = ""
    return render_template("index.html.j2", total=totals, notice=notice)
