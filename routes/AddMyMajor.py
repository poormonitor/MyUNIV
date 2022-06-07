from flask import Blueprint, session, request
from func import get_what_i_can_choose, get_what_i_can_choose_most, login_required_ajax
from models.Major import Major
from models.Univ import Univ
from models.Rank import Rank
from models.Must import Must
from models.User import User
from models import db

add_my_major_bp = Blueprint('AddMyMajor', __name__)


@add_my_major_bp.route('/my/add', methods=['GET'])
@login_required_ajax
def addmymajor():
    my = session["my"]
    if request.args.get("action") == "id":
        id = int(request.args.get("mid"))
        my.append(id)
    elif request.args.get("action") == "delete":
        id = int(request.args.get("mid"))
        my.remove(id)
    elif request.args.get("action") == "del":
        my = []
    elif request.args.get("action") == "query":
        page = int(
            request.args.get("page")) if "page" in request.args else None
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
        if "rank" in request.args and request.args["rank"] != "":
            rank = int(request.args["rank"])
            if not info["rank_range"]:
                result = result.filter(Rank.rank >= rank).filter(
                    Rank.rank != 0)
                result = result.order_by(db.func.abs(Rank.rank).asc())
            else:
                result = result.filter(
                    rank - info["rank_range"] <= Rank.rank,
                    Rank.rank <= rank + info["rank_range"]).filter(
                        Rank.rank != 0)
                result = result.order_by(db.func.abs(Rank.rank - rank).asc())
            info["rank"] = rank
        else:
            result = result.order_by(Univ.sid.asc())
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
                    Must.year == info["standard"])).group_by(Major.mid)
        if "province" in request.args and request.args["province"] != "":
            province = info["province"] = list(
                map(int, request.args.getlist("province")))
            result = result.filter(Univ.province.in_(province))
        if "sort" in request.args and request.args["sort"] != "":
            info["sort"] = request.args["sort"]
            result = result.filter(
                db.or_(
                    Must.include.contains(i) for i in info["sort"].split(" ")))
        if page:
            result = result.offset((page - 1) * 50).limit(50)
        result = result.all()
        for i in result:
            my.append(i[0].mid)
    session["my"] = my
    my = ",".join(list(map(str, list(set(my)))))
    User.query.filter_by(uid=session["uid"]).update({"mymajor": my})
    return "success"
