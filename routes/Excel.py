from models.Major import Major
from models.Univ import Univ
from models.Rank import Rank
from models.Must import Must
from models.Conne import Conne
from models import db
from flask import Blueprint, request, session, make_response
from func import (
    login_required,
    get_must_string,
    freezeDict,
    findResult,
    findNearestMust,
)
import pandas as pd
import hashlib
import io

excel_bp = Blueprint("Excel", __name__)


@excel_bp.route("/excel", methods=["GET"])
@login_required
def excel():
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
    result = db.session.query(Major, Univ, Rank, Must, Conne)
    result = result.outerjoin(Major, Major.mid == Rank.mid)
    result = result.outerjoin(Univ, Univ.sid == Major.sid)
    result = result.outerjoin(Conne, db.and_(Conne.mid == Major.mid))
    result = result.outerjoin(
        Must, db.and_(Conne.mmid == Must.mmid, Conne.year == Must.year)
    )

    if "my" in request.args and request.args.get("my") == "1":
        info = session["my"]
        year = int(request.args.get("year"))
        standard = int(request.args.get("standard"))
        result = result.filter(Major.mid.in_(info))
        result = result.filter(Rank.year == year)
        result = result.filter(Must.year == standard)
        result = result.group_by(Major.mid)
        result = result.order_by(Rank.score.desc())
        info = {"info": info, year: year, standard: standard}
    else:
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

        _, result = findResult(None, freezeDict(info))

    result = [
        i if i[3] else (i[0], i[1], i[2], findNearestMust(i[0], year)) for i in result
    ]

    data = [
        (
            item[1].uname,
            item[0].mname,
            item[2].schedule,
            item[2].year,
            item[2].rank,
            item[2].score,
            get_must_string(item[3].must) if item[3] else "",
            item[3].year if item[3] else "",
        )
        for item in result
    ]

    df = pd.DataFrame(
        data, columns=["学校名称", "专业名称", "招生计划", "年份", "位次号", "录取分数", "选考科目", "选考科目标准"]
    )

    filename = "MyUNIV_Export_" + hashlib.md5(str(info).encode()).hexdigest() + ".xlsx"
    out = io.BytesIO()
    writer = pd.ExcelWriter(out, engine="openpyxl")
    df.to_excel(excel_writer=writer, sheet_name="志愿信息", index=False)
    writer.close()
    response = make_response(out.getvalue())
    response.headers["Content-Disposition"] = "attachment; filename*=utf-8''{}".format(
        filename
    )
    response.headers["Content-type"] = "application/x-xlsx"

    return response
