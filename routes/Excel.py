from models.Major import Major
from models.Univ import Univ
from models.Rank import Rank
from models.Tag import Tag
from models.Must import Must
from models import db
from flask import Blueprint, render_template, url_for, request, session, make_response
from func import login_required, get_what_i_can_choose, get_must_string, get_what_i_can_choose_most
from const import majors, provinces
import pandas as pd
import hashlib
import io

excel_bp = Blueprint('Excel', __name__)


@excel_bp.route('/excel', methods=['GET'])
@login_required
def excel():
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
        if info["accordation"]:
            what_i_can = get_what_i_can_choose_most(mymust)
            result = result.order_by(Must.must.desc())
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
    result = result.all()
    data = [(item[1].uname, item[0].mname, item[2].schedule,
             item[2].year, item[2].rank, item[2].score,
             get_must_string(item[3].must) if item[3] else "",
             item[3].year if item[3] else "") for item in result]
    df = pd.DataFrame(data,
                      columns=[
                          '学校名称', '专业名称', '招生计划', '年份', '位次号', '录取分数', '选考科目',
                          '选考科目标准'
                      ])
    filename = hashlib.md5(str(info).encode()).hexdigest() + ".xlsx"
    out = io.BytesIO()
    writer = pd.ExcelWriter(out, engine='openpyxl')
    df.to_excel(excel_writer=writer, sheet_name='志愿信息', index=False)
    writer.save()
    writer.close()
    response = make_response(out.getvalue())
    response.headers[
        "Content-Disposition"] = "attachment; filename*=utf-8''{}".format(
            filename)
    response.headers["Content-type"] = "application/x-xlsx"
    return response
