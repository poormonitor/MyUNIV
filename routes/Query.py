from models.Major import Major
from models.Univ import Univ
from models.Rank import Rank
from models import db
from flask import Blueprint, render_template, redirect, url_for, request, session
from func import islogin, login_required

query_bp = Blueprint('Query', __name__)


@query_bp.route('/query', methods=['GET'])
@login_required
def query():
    page = int(request.args.get("page")) if "page" in request.args else 1
    last_year = a.year if (a := Rank.query.order_by(
        Rank.year.desc()).first()) else ""
    result = db.session.query(Major, Univ, Rank).filter(
        Univ.sid == Major.sid, Major.mid == Rank.mid).order_by(Univ.sid)
    info = {
        "rank": "",
        "year": last_year,
        "school": "",
        "major": "",
        "rank_range": 1000
    }
    if "school" in request.args and request.args["school"] != "":
        for i in request.args["school"].split(" "):
            result = result.filter(Univ.uname.like("%" + i + "%"))
        info["school"] = request.args["school"]
    if "major" in request.args and request.args["major"] != "":
        result = result.filter(
            Major.mname.like("%" + request.args["major"] + "%"))
        info["major"] = request.args["major"]
    if "year" in request.args and request.args["year"] != "":
        info["year"] = int(request.args["year"])
    result = result.filter(Rank.year == info["year"])
    if "rank_range" in request.args and request.args["rank_range"] != "":
        rank_range = int(request.args["rank_range"])
        info["rank_range"] = rank_range
    if "rank" in request.args and request.args["rank"] != "":
        rank = int(request.args["rank"])
        result = result.filter(rank - info["rank_range"] <= Rank.rank,
                               Rank.rank <= rank + info["rank_range"])
        info["rank"] = rank
    cnt = len(result.all()) // 50 + 1
    result = result.offset((page - 1) * 50).limit(50).all()
    urls = [
        str(url_for('Query.query', page=i, **info))
        for i in (1, page - 1, page, page + 1, cnt)
    ]
    return render_template(
        'query.html',
        result=result,
        session=session,
        request=info,
        page=page,
        cnt=cnt,
        string=urls,
    )