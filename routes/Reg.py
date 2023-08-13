from models.User import User
from flask import Blueprint, render_template, request, session, redirect, url_for
from models import db
from func import not_login_required
from const import majors
from hashlib import md5

reg_bp = Blueprint("Reg", __name__)


@reg_bp.route("/reg", methods=["POST", "GET"])
@not_login_required
def reg():
    if request.method == "GET":
        import os

        session["nonce"] = os.urandom(16).hex()
        session["csrf"] = os.urandom(16).hex()
        error = request.args.get("error", None)
        error = (
            {
                "1": "账号已存在",
                "2": "参数错误",
            }[error]
            if error
            else None
        )
        return render_template(
            "reg.html.j2",
            csrf=session["csrf"],
            error=error,
            must_string=enumerate(majors[1:]),
        )

    uid = request.form["uid"]
    name = request.form["name"]
    passwd = request.form["passwd"]
    must = int("".join(request.form.getlist("mymust")))
    csrf = request.form["csrf"]
    result = User.query.filter_by(uid=uid).first()
    if result:
        return redirect(url_for("Reg.reg", error=1))
    if csrf != session["csrf"]:
        return redirect(url_for("Reg.Reg", error=2))
    new_user = User(uid=uid, name=name, password=passwd, admin=False, must=must)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for("Login.login", suc=1))
