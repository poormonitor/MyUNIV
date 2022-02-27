from flask import Blueprint, redirect, render_template, session, request, url_for
from func import isadmin, valid_csrf
from models import db
from models.Major import Major
from models.Univ import Univ
from models.Tag import Tag
import pandas as pd
import re
import os

add_data_bp = Blueprint('AddData', __name__)


@add_data_bp.route('/adddata', methods=['GET', 'POST'])
def adddata():
    if isadmin():
        if request.method == "GET":
            session['csrf'] = os.urandom(16).hex()
            return render_template('adddata.html', session=session, csrf=session["csrf"])
        if not valid_csrf():
            return redirect(url_for('AddData.adddata'))
        xlsx = request.files['xlsx']
        year = request.form["year"]
        """浙江大学(一流大学建设高校)"""
        df = pd.read_excel(xlsx)
        for i in df.values:
            univ_id = int(i[0])
            univ_name = i[1]
            major = i[3]
            schedule = i[4]
            rank = i[6]
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
            if Major.query.filter_by(sid=univ_id, mname=major,
                                     year=year).first() is None:
                db.session.add(
                    Major(sid=univ_id,
                          mtags="",
                          must=0,
                          mname=major,
                          schedule=schedule,
                          rank=rank,
                          year=year))
            else:
                db.session.query(Major).filter(Major.sid == univ_id,
                                               Major.mname == major,
                                               Major.year == year).update({
                                                   "schedule":
                                                   schedule,
                                                   "rank":
                                                   rank
                                               })
        db.session.commit()
    return redirect(url_for('Index.index'))
