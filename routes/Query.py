from models.Major import Major
from models.Univ import Univ
from models import db
from flask import Blueprint, render_template, redirect, url_for, request, session
from func import islogin

query_bp = Blueprint('Query', __name__)


@query_bp.route('/query', methods=['GET'])
def query():
    if islogin():
        result = db.session.query(
            Major, Univ).filter(Univ.sid == Major.sid).order_by(Univ.sid)
        info = {"rank": "", "year": "", "school": "", "major": ""}
        if "school" in request.args and request.args["school"] != "":
            result = result.filter(
                Univ.uname.like("%" + request.args["school"] + "%"))
            info["school"] = request.args["school"]
        if "major" in request.args and request.args["major"] != "":
            result = result.filter(
                Major.mname.like("%" + request.args["major"] + "%"))
            info["major"] = request.args["major"]
        if "year" in request.args and request.args["year"] != "":
            result = result.filter(Major.year == int(request.args["year"]))
            info["year"] = request.args["year"]
        if "rank" in request.args and request.args["rank"] != "":
            result = result.filter(
                int(request.args["rank"]) -
                1000 <= Major.rank <= int(request.args["rank"]) + 1000)
            info["rank"] = request.args["rank"]
        result = result.limit(50).all()
        return render_template('query.html',
                               result=result,
                               session=session,
                               request=info)
    return redirect(url_for('Index.index'))
