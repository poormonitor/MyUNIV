from models.Rank import Rank
from models.Tag import Tag
from models.Must import Must
from models import db
from flask import Blueprint, render_template, url_for, request, session
from func import get_must_string, findResult, freezeDict
from const import majors, provinces

query_bp = Blueprint("Query", __name__)


@query_bp.route("/query", methods=["GET"])
def query():
    last_year = (
        a.year
        if (
            a := db.session.query(Rank.year)
            .distinct()
            .order_by(Rank.year.desc())
            .first()
        )
        else 0
    )
    page = int(request.args.get("page")) if "page" in request.args else 1
    info = {
        "rank": "",
        "year": last_year,
        "school": "",
        "major": "",
        "rank_range": "",
        "utags": "",
        "musts": 0,
        "province": [],
        "utags": [],
        "nutags": [],
        "mymust": [],
        "sort": "",
        "standard": "",
        "accordation": 0,
    }
    if "school" in request.args and request.args["school"] != "":
        info["school"] = request.args["school"]
    if "major" in request.args and request.args["major"] != "":
        info["major"] = request.args["major"]
    if "year" in request.args and request.args["year"] != "":
        info["year"] = int(request.args["year"])
    if "rank_range" in request.args and request.args["rank_range"] != "":
        rank_range = int(request.args["rank_range"])
        info["rank_range"] = rank_range
    if "rank" in request.args and request.args["rank"] != "":
        rank = int(request.args["rank"])
        info["rank"] = rank
    if "accordation" in request.args and request.args["accordation"] == "1":
        info["accordation"] = 1
    if "mymust" in request.args and request.args["mymust"] != "":
        mymust = request.args.getlist("mymust")
        info["mymust"] = list(map(int, mymust))
    if "utags" in request.args and request.args["utags"] != "":
        utags = list(map(int, request.args.getlist("utags")))
        utags.sort()
        info["utags"] = utags
    if "nutags" in request.args and request.args["nutags"] != "":
        nutags = list(map(int, request.args.getlist("nutags")))
        nutags.sort()
        info["nutags"] = nutags
    if "standard" in request.args and request.args["standard"] != "":
        info["standard"] = int(request.args["standard"])
    if not info["standard"]:
        last_year_must = (
            a.year if (a := Must.query.order_by(Must.year.desc()).first()) else 0
        )
        info["standard"] = last_year_must
    if "province" in request.args and request.args["province"] != "":
        info["province"] = list(map(int, request.args.getlist("province")))
    if "sort" in request.args and request.args["sort"] != "":
        info["sort"] = request.args["sort"]
    count, result = findResult(page, freezeDict(info))
    cnt = (count - 1) // 50 + 1 if count > 0 else 1
    rank_year_available = [
        i.year for i in Rank.query.group_by(Rank.year).order_by(Rank.year.desc()).all()
    ]
    must_year_available = [
        i.year for i in Must.query.group_by(Must.year).order_by(Must.year.desc()).all()
    ]
    musts = [(get_must_string(i[3].must), i[3].year) if i[3] else "" for i in result]
    urls = [
        str(url_for("Query.query", page=i, **info))
        for i in (1, page - 2, page - 1, page, page + 1, page + 2, cnt)
    ]
    all_tags = Tag.query.all()
    return render_template(
        "query.html.j2",
        result=enumerate(result),
        info=info,
        page=page,
        cnt=cnt,
        string=urls,
        provinces=provinces.items(),
        must_string=enumerate(majors[1:]),
        utags=all_tags,
        musts=musts,
        rank_years=rank_year_available,
        must_standard=must_year_available,
        count=count,
        mymust=session.get("must", ""),
    )
