from models.Major import Major
from models.Univ import Univ
from models.Rank import Rank
from models.Tag import Tag
from models.Must import Must
from models import db
from flask import Blueprint, render_template, url_for, request
from func import login_required
from const import majors, provinces
from itertools import combinations

query_bp = Blueprint('Query', __name__)


@query_bp.route('/query', methods=['GET'])
@login_required
def query():
    page = int(request.args.get("page")) if "page" in request.args else 1
    last_year = a.year if (a := Rank.query.order_by(
        Rank.year.desc()).first()) else ""
    result = db.session.query(Major, Univ, Rank).filter(
        Univ.sid == Major.sid, Major.mid == Rank.mid).outerjoin(
            Must, Must.mid == Major.mid).order_by(Univ.sid)
    info = {
        "rank": "",
        "year": last_year,
        "school": "",
        "major": "",
        "rank_range": "",
        "utags": "",
        "musts": 0
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
        if not info["rank_range"]:
            info["rank_range"] = 1000
        rank = int(request.args["rank"])
        result = result.filter(
            rank - info["rank_range"] <= Rank.rank,
            Rank.rank <= rank + info["rank_range"]).filter(Rank.rank != 0)
        info["rank"] = rank
    if "utags" in request.args and request.args["utags"] != "":
        utags = request.args["utags"].split(" ")
        tags = []
        tagnames = []
        for i in utags:
            tagnames.append(i)
            if (a := db.session.query(Tag).filter(
                    Tag.tname.like("%" + i + "%")).first()) is not None:
                tags.append(a.tid)
        tags.sort()
        for i in tags:
            result = result.filter(Univ.utags.like("%," + str(i) + ",%"))
        info["utags"] = ",".join(tagnames)
    if "mymust" in request.args and request.args["mymust"] != "":
        mymust = list(request.args["mymust"])
        info["mymust"] = list(map(int, mymust))
        mymust = ["0"] + mymust
        mymust = ["0"] + list(combinations(mymust, 3)) + list(
            combinations(mymust, 2)) + list(combinations(mymust, 1))
        mymust = [int("".join(i)) for i in mymust]
        for i in mymust:
            result = result.filter(Must.must.in_(mymust))
    cnt = len(result.all()) // 50 + 1
    result = result.offset((page - 1) * 50).limit(50).all()
    urls = [
        str(url_for('Query.query', page=i, **info))
        for i in (1, page - 1, page, page + 1, cnt)
    ]
    return render_template('query.html',
                           result=result,
                           request=info,
                           info=info,
                           page=page,
                           cnt=cnt,
                           string=urls,
                           provinces=provinces.items(),
                           must_string=enumerate(majors[1:]))
