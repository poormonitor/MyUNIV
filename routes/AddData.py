from flask import Blueprint, redirect, render_template, session, request, url_for
from func import isadmin, valid_csrf, admin_required
from models import db
from models.Major import Major
from models.Univ import Univ
from models.Tag import Tag
from models.Rank import Rank
from tempfile import NamedTemporaryFile
import pandas as pd
import xlrd
import re
import os

add_data_bp = Blueprint('AddData', __name__)


@add_data_bp.route('/adddata', methods=['GET', 'POST'])
@admin_required
def adddata():
    if request.method == "GET":
        session['csrf'] = os.urandom(16).hex()
        return render_template('adddata.html',
                               session=session,
                               csrf=session["csrf"])
    if not valid_csrf():
        return redirect(url_for('AddData.adddata'))
    xlsx = request.files['xlsx']
    year = int(request.form["year"])
    """
    fd = NamedTemporaryFile()
    xlsx.save(fd.name)
    """
    data = pd.read_excel(xlsx)
    for i in data.values:
        univ_id = int(i[0])
        univ_name = str(i[1])
        major = str(i[3])
        schedule = int(i[4])
        rank = int(i[6]) if i[6] == i[6] else ""
        if Univ.query.filter_by(sid=univ_id).first() is None:
            tags = re.findall(r'(?<=[\(]).*?(?=[\)])', univ_name)
            tids = []
            for j in tags:
                if Tag.query.filter_by(tname=j).first() is None:
                    db.session.add(Tag(tname=j))
                tids.append(Tag.query.filter_by(tname=j).first().tid)
            tids = ",".join(str(i) for i in tids)
            univ_name = univ_name.split("(")[0]
            db.session.add(
                Univ(sid=univ_id, uname=univ_name, utags=tids, province=1))
        if Major.query.filter_by(sid=univ_id, mname=major).first() is None:
            db.session.add(
                Major(sid=univ_id, mtags="", mname=major, schedule=schedule))
            mid = Major.query.filter_by(sid=univ_id, mname=major).first().mid
            db.session.add(Rank(mid=mid, year=year, rank=rank))
        else:
            mid = db.session.query(Major).filter(Major.sid == univ_id,
                                                 Major.mname == major)
            mid.update({"schedule": schedule})
            db.session.query(Rank).filter(Rank.mid == mid.first().mid,
                                          Rank.year == year).update(
                                              {"rank": rank})
    db.session.commit()
    return redirect(url_for('Index.index'))
