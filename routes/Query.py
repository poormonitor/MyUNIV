from models.Major import Major
from models.Univ import Univ
from models.Rank import Rank
from models.Tag import Tag
from models.Must import Must
from models import db
from flask import Blueprint, render_template, url_for, request, session
from func import login_required, get_what_i_can_choose, get_must_string, get_what_i_can_choose_most
from const import majors, provinces

query_bp = Blueprint('Query', __name__)


@query_bp.route('/query', methods=['GET'])
@login_required
def query():
    page = int(request.args.get("page")) if "page" in request.args else 1
    last_year = a.year if (a := db.session.query(
        Rank.year).distinct().order_by(Rank.year.desc()).first()) else ""
    result = db.session.query(Major, Univ, Rank, Must)
    result = result.outerjoin(Major, Major.mid == Rank.mid)
    result = result.outerjoin(Univ, Univ.sid == Major.sid)
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
        "sort": "",
        "standard": "",
        "accordation": 0
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
        if not info["rank_range"]:
            result = result.filter(Rank.rank >= rank).filter(Rank.rank != 0)
            result = result.order_by(db.func.abs(Rank.rank).asc())
        else:
            result = result.filter(
                rank - info["rank_range"] <= Rank.rank,
                Rank.rank <= rank + info["rank_range"]).filter(Rank.rank != 0)
            result = result.order_by(db.func.abs(Rank.rank - rank).asc())
        info["rank"] = rank
    else:
        result = result.order_by(Univ.sid.asc())
    if "accordation" in request.args and request.args["accordation"] == "1":
        info["accordation"] = 1
    if "mymust" in request.args and request.args["mymust"] != "":
        mymust = request.args.getlist("mymust")
        info["mymust"] = list(map(int, mymust))
        mymust = "".join(mymust)
        result = result.order_by(Must.must.desc())
        if info["accordation"]:
            what_i_can = get_what_i_can_choose_most(mymust)
        else:
            what_i_can = get_what_i_can_choose(mymust)
        result = result.filter(Must.must.in_(what_i_can))
    elif "must" in session and session["must"] != 0:
        mymust = str(session["must"])
        info["mymust"] = list(map(int, list(mymust)))
        what_i_can = get_what_i_can_choose(mymust)
        result = result.filter(Must.must.in_(what_i_can))
    if "utags" in request.args and request.args["utags"] != "":
        utags = list(map(int, request.args.getlist("utags")))
        utags.sort()
        condition = db.or_(
            Univ.utags.like("%," + str(i) + ",%") for i in utags)
        result = result.filter(condition)
        info["utags"] = utags
    if "nutags" in request.args and request.args["nutags"] != "":
        nutags = list(map(int, request.args.getlist("nutags")))
        nutags.sort()
        ncondition = db.not_(
            db.and_(Univ.utags.like("%," + str(i) + ",%") for i in nutags))
        result = result.filter(ncondition)
        info["nutags"] = nutags
    if "standard" in request.args and request.args["standard"] != "":
        info["standard"] = int(request.args["standard"])
    if not info["standard"]:
        last_year_must = a.year if (a := Must.query.order_by(
            Must.year.desc()).first()) else ""
        info["standard"] = last_year_must
    result = result.outerjoin(
        Must,
        db.and_(Must.sid == Major.sid, Major.mname.contains(Must.mname),
                Must.year == info["standard"]))
    if "province" in request.args and request.args["province"] != "":
        province = info["province"] = list(
            map(int, request.args.getlist("province")))
        result = result.filter(Univ.province.in_(province))
    if "sort" in request.args and request.args["sort"] != "":
        info["sort"] = request.args["sort"]
        result = result.filter(
            db.or_(Must.include.contains(i) for i in info["sort"].split(" ")))
    count = result.count()
    cnt = count // 50 + 1
    result = result.offset((page - 1) * 50).limit(50).all()
    musts = [(get_must_string(i[3].must), i[3].year) if i[3] else ""
             for i in result]
    urls = [
        str(url_for('Query.query', page=i, **info))
        for i in (1, page - 1, page, page + 1, cnt)
    ]
    all_tags = Tag.query.all()
    rank_year_available = [
        i.year for i in Rank.query.group_by(Rank.year).order_by(
            Rank.year.desc()).all()
    ]
    must_year_available = [
        i.year for i in Must.query.group_by(Must.year).order_by(
            Must.year.desc()).all()
    ]
    return render_template('query.html',
                           result=enumerate(result),
                           request=info,
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
                           count=count)
