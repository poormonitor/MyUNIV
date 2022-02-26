from flask import Blueprint, redirect, render_template, session, request
from func import isadmin
from models import db
from models.Major import Major
from models.Univ import Univ
from models.Tag import Tag
import pandas as pd
import re

add_data_bp = Blueprint('AddData', __name__)


@add_data_bp.route('/adddata', methods=['GET', 'POST'])
def adddata():
    if isadmin():
        if request.method == "GET":
            return render_template('adddata.html', session=session)
        xlsx = request.files['xlsx']
        year = request.form["year"]
        """浙江大学(一流大学建设高校)"""
        df = pd.read_excel(xlsx)
        print(df)
        for i in df:
            univ = int(i[0])
            univ_name = i[1].split("(")[0]
            major = i[3]
            schedule = i[4]
            rank = i[6]
            db.seesion.delete(Major(sid=univ, mname=major))
            if Univ.query.filter_by(univ=univ).first() is None:
                tags = re.matchall(r'(?<=[\(]).*?(?=[\)])', univ)
                tids = []
                for j in tags:
                    if Tag.query.filter_by(tag=j).first() is None:
                        db.session.add(Tag(tag=j))
                    tids.append(Tag.query.filter_by(tag=j).first().tid)
                tids = ",".join(str(i) for i in tids)
                db.session.add(
                    Univ(sid=univ, uname=univ_name, utags=tids, province=1))
            db.session.add(
                Major(sid=univ,
                      mname=major,
                      schedule=schedule,
                      rank=rank,
                      year=year))
        db.session.commit()
    else:
        return redirect('/')
