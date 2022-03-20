from flask import Blueprint, redirect, render_template, session, request, url_for
from func import valid_csrf, admin_required
import os

add_data_bp = Blueprint('AddData', __name__)


@add_data_bp.route('/adddata', methods=['GET', 'POST'])
@admin_required
def adddata():
    if request.method == "GET":
        session['csrf'] = os.urandom(16).hex()
        return render_template('adddata.html', csrf=session["csrf"])
    if not valid_csrf():
        return redirect(url_for('AddData.adddata'))
    year = int(request.form["year"])
    xlsx = request.files['xlsx']
    process_excel(xlsx, year)
    return redirect(url_for('Index.index'))


def process_excel(xlsx, year):
    from models import db
    from models.Major import Major
    from models.Univ import Univ
    from models.Must import Must
    from models.Tag import Tag
    from models.Rank import Rank
    from pandas import read_excel
    from const import allow_tags, provinces, majors
    from func import get_school_name
    import re
    data = read_excel(xlsx)
    if "位次" in data.columns.tolist():
        univs = {i.uname: i.sid for i in Univ.query.all()}
        pattern = re.compile(r'(?<=[\(])(%s).*?(?=[\)])' %
                             "|".join(allow_tags))
        tags = {i.tname: i.tid for i in Tag.query.all()}
        for i in data.values:
            univ_name = get_school_name(i[1])
            major = i[3]
            schedule = i[4]
            score = i[5]
            rank = i[6] if i[6] == i[6] else 0
            if univ_name not in univs:
                tag = pattern.findall(i[1])
                tids = []
                for j in tag:
                    if j not in tags:
                        t = Tag(tname=j)
                        db.session.add(t)
                        db.session.flush()
                        tid = t.tid
                        tags[j] = tid
                    else:
                        tid = tags[j]
                    tids.append(tid)
                tids = "," + ",".join(str(i) for i in tids) + ","
                univ = Univ(uname=univ_name, utags=tids, province=0)
                db.session.add(univ)
                db.session.flush()
                univs[univ_name] = univ.sid
            univ_id = univs[univ_name]
            if (b := Major.query.filter_by(sid=univ_id,
                                           mname=major).first()) is None:
                b = Major(sid=univ_id, mname=major)
                db.session.add(b)
                db.session.flush()
            if (a := db.session.query(Rank).filter(Rank.mid == b.mid, Rank.year
                                                   == year).first()) is None:
                db.session.add(
                    Rank(mid=b.mid,
                         year=year,
                         rank=rank,
                         schedule=schedule,
                         score=score))
                db.session.flush()
            else:
                a.rank = rank
                a.schedule = schedule
                db.session.flush()
    elif "选考科目要求" in data.columns.tolist():
        univs = {i.uname: i.sid for i in Univ.query.all()}
        for i in data.values:
            province = i[0]
            univ_name = get_school_name(i[1])
            major = i[2]
            include = i[3] if i[3] == i[3] else ""
            must = int("".join(
                [str(majors.index(j)) for j in i[5].split("(")[0].split(",")]))
            if must != 0:
                must = int(re.search(r"\d+", i[5]).group(0) + str(must))
            province_id = list(provinces.keys())[list(
                provinces.values()).index(province)]
            if univ_name not in univs:
                univ = Univ(uname=univ_name, province=province_id)
                db.session.add(univ)
                db.session.flush()
                univ_id = univ.sid
                univs[univ_name] = univ_id
            else:
                univ = db.session.query(Univ).filter(
                    Univ.uname == univ_name).first()
                univ.province = province_id
                univ_id = univ.sid
                db.session.flush()
            if (a := Must.query.filter_by(mname=major, sid=univ_id,
                                          year=year).first()) is None:
                db.session.add(
                    Must(mname=major,
                         year=year,
                         sid=univ_id,
                         must=must,
                         include=include))
            else:
                a.must = must
                a.include = include
            db.session.flush()
    db.session.commit()