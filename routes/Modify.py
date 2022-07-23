from flask import Blueprint, redirect, render_template, session, request, url_for
from func import login_required, valid_csrf
from const import majors
from models import db
from models.User import User
import os

modify_bp = Blueprint("Modify", __name__)


@modify_bp.route("/modify", methods=["GET", "POST"])
@login_required
def modify():
    if request.method == "GET":
        error = None
        if "error" in request.args:
            error = {"1": "原密码错误"}[request.args["error"]]
        session["csrf"] = os.urandom(16).hex()
        mymust = list(map(int, list(str(session["must"]))))
        return render_template(
            "modify.html.j2",
            csrf=session["csrf"],
            error=error,
            must_string=enumerate(majors[1:]),
            mymust=mymust,
        )
    if not valid_csrf():
        return redirect(url_for("Modify.modify"))
    tp = request.form["action"]
    if tp == "password":
        result = User.query.filter_by(uid=session["uid"]).first()
        old_password = request.form["old_password"]
        new_password = request.form["new_password"]
        if result.passwd != old_password:
            return redirect(url_for("Modify.modify", error="1"))
        result.passwd = new_password
        session["notice"] = "密码修改成功"
    elif tp == "must":
        result = User.query.filter_by(uid=session["uid"]).first()
        result.must = (
            int("".join(request.form.getlist("mymust")))
            if "mymust" in request.form
            else 0
        )
        session["must"] = result.must
        db.session.flush()
        session["notice"] = "选考科目修改成功"
    db.session.commit()
    return redirect(url_for("Index.index"))
