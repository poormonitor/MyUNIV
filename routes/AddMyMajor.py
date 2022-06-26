from flask import Blueprint, session, request
from func import (
    login_required_ajax,
    findResult,
    freezeDict,
)
from models.Rank import Rank
from models.Must import Must
from models.User import User
from models import db

add_my_major_bp = Blueprint("AddMyMajor", __name__)


@add_my_major_bp.route("/my/add", methods=["GET"])
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
        page = int(request.args.get("page")) if "page" in request.args else None
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
        _, result = findResult(page, freezeDict(info))
        if "del" not in request.args:
            for i in result:
                my.append(i[0].mid)
        else:
            for i in result:
                if (mid := i[0].mid) in my:
                    my.remove(mid)
    session["my"] = my
    my = ",".join(list(map(str, list(set(my)))))
    User.query.filter_by(uid=session["uid"]).update({"mymajor": my})
    return "success"
