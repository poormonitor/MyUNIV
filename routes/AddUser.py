from flask import Blueprint, redirect, render_template, session, request, url_for
from func import admin_required, valid_csrf
from models import db
from models.User import User
from hashlib import md5
import re
import os

add_user_bp = Blueprint("AddUser", __name__)


@add_user_bp.route("/adduser", methods=["GET", "POST"])
@admin_required
def adduser():
    if request.method == "GET":
        from func import get_mymust_string

        session["csrf"] = os.urandom(16).hex()
        page = int(request.args.get("page")) if "page" in request.args else 1
        info = {"checkString": ""}
        result = User.query
        if "checkString" in request.args and request.args["checkString"] != "":
            info["checkString"] = request.args["checkString"]
            result = result.filter(
                db.or_(
                    User.name.contains(info["checkString"]),
                    User.uid.contains(info["checkString"]),
                )
            )
        count = result.count()
        cnt = (count - 1) // 50 + 1 if count > 0 else 1
        users = result.offset((page - 1) * 50).limit(50).all()
        urls = [
            str(url_for("AddUser.adduser", page=i, **info))
            for i in (1, page - 1, page, page + 1, cnt)
        ]
        return render_template(
            "adduser.html.j2",
            csrf=session["csrf"],
            users=users,
            cnt=cnt,
            string=urls,
            page=page,
            info=info,
            get_func=get_mymust_string,
        )
    if not valid_csrf():
        return redirect(url_for("AddUser.adduser"))
    typ = request.form["action"]
    if typ == "add":
        users = request.form.get("users")
        tp = int(request.form.get("type"))
        for line in users.splitlines():
            items = re.split(",| |\t", line)
            if (a := User.query.filter_by(uid=items[0]).first()) is None:
                passwd = md5(str(items[2]).encode("utf-8")).hexdigest()
                db.session.add(
                    User(
                        uid=items[0],
                        name=items[1],
                        password=passwd,
                        admin=True if tp else False,
                        must=int(items[3]) if len(items) > 3 else 0,
                    )
                )
            else:
                passwd = md5(str(items[2]).encode("utf-8")).hexdigest()
                a.password = passwd
                a.name = items[1]
                a.admin = True if tp else False
                if len(items) > 3:
                    a.must = int(items[3])
    elif typ == "change":
        users = request.form.get("users")
        for line in users.splitlines():
            items = re.split(",| |\t", line)
            if (a := User.query.filter_by(uid=items[0]).first()) is not None:
                a.must = int(items[1])
                db.session.flush()
    elif typ == "del":
        user = request.form.get("user")
        if (a := User.query.filter_by(uid=user).first()) is not None:
            db.session.delete(a)
        db.session.commit()
        return "success", 200
    elif typ == "delete":
        users = request.form.get("users")
        for line in users.splitlines():
            item = re.split(",| |\t", line)[0]
            if (a := User.query.filter_by(uid=item).first()) is not None:
                db.session.delete(a)
    elif typ == "passwd":
        user = request.form.get("user")
        passwd = request.form.get("passwd")
        if (a := User.query.filter_by(uid=user).first()) is not None:
            a.passwd = passwd
            db.session.flush()
    elif typ == "set":
        user = request.form.get("user")
        if (a := User.query.filter_by(uid=user).first()) is not None:
            a.admin = not a.admin
            db.session.commit()
            result = "是" if a.admin else "否"
            return result, 200
    db.session.commit()
    return redirect(url_for("AddUser.adduser"))
