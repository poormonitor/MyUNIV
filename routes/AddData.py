from flask import Blueprint, redirect, render_template, session, request, url_for
from func import get_school_name, valid_csrf, admin_required
from models import db
from models.Major import Major
from models.Univ import Univ
from models.Must import Must
from models.Tag import Tag
from models.Rank import Rank
from pandas import read_excel
from const import allow_tags, provinces, majors
import re
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
    type = int(request.form["type"])
    year = int(request.form["year"])
    xlsx = request.files['xlsx']
    process_excel(xlsx, year, type)
    return redirect(url_for('Index.index'))


def process_excel(xlsx, year, type):
    data = read_excel(xlsx)
    univs = [i.uname for i in Univ.query.all()]
    if type == 1:
        pattern = re.compile(r'(?<=[\(])(%s).*?(?=[\)])' %
                             "|".join(allow_tags))
        tags = {i.tname: i.tid for i in Tag.query.all()}
        for i in data.values:
            univ_id = i[0]
            univ_name = get_school_name(i[1])
            major = i[3]
            schedule = i[4]
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
                univs.append(univ_id)
                db.session.add(
                    Univ(uname=univ_name, utags=tids, province=0))
                univs.append(univ_name)
            if Major.query.filter_by(sid=univ_id, mname=major).first() is None:
                m = Major(sid=univ_id, mtags="", mname=major)
                db.session.add(m)
                db.session.flush()
                db.session.add(
                    Rank(mid=m.mid, year=year, rank=rank, schedule=schedule))
            else:
                mid = db.session.query(Major).filter(Major.sid == univ_id,
                                                     Major.mname == major)
                db.session.query(Rank).filter(Rank.mid == mid.first().mid,
                                              Rank.year == year).update({
                                                  "rank":
                                                  rank,
                                                  "schedule":
                                                  schedule
                                              })
    elif type == 2:
        for i in data.values:
            province = i[0]
            univ_name = i[1]
            major = i[2]
            include = i[3] if i[3] == i[3] else ""
            must = int("".join(
                [str(majors.index(j)) for j in i[5].split("(")[0].split(",")]))
            if must != 0:
                must = int(re.search(r"\d+", i[5]).group(0) + str(must))
            province_id = list(provinces.keys())[list(
                provinces.values()).index(province)]
            if univ_name not in univs:
                univs.append(univ_name)
                univ = Univ(uname=univ_name, province=province_id)
                db.session.add(univ)
                db.session.flush()
                univ_id = univ.sid
            else:
                univ = db.session.query(Univ).filter(
                    Univ.uname == univ_name).first()
                univ.province = province_id
                univ_id = univ.sid
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
            print(univ_id, major, must, include)
    db.session.commit()