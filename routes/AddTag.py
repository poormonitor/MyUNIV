from flask import Blueprint, redirect, render_template, session, request, url_for
from func import get_school_name, unifyBracket, valid_csrf, admin_required
from models import db
from models.Tag import Tag
from models.Univ import Univ
import os

add_tag_bp = Blueprint("AddTag", __name__)


@add_tag_bp.route("/addtag", methods=["GET", "POST"])
@admin_required
def addtag():
    if request.method == "GET":
        session["csrf"] = os.urandom(16).hex()
        return render_template(
            "addtag.html.j2",
            csrf=session["csrf"],
        )
    if not valid_csrf():
        return redirect(url_for("AddTag.addtag"))
    schools = request.form["schools"]
    tag = request.form["tag"]
    if (a := Tag.query.filter_by(tname=tag).first()) is None:
        a = Tag(tname=tag)
        db.session.add(a)
        db.session.flush()
    tag_id = a.tid
    for i in schools.splitlines():
        i, _ = get_school_name(i)
        i = unifyBracket(i)
        if (a := Univ.query.filter_by(uname=i).first()) is None:
            a = Univ(uname=i)
            db.session.add(a)
            db.session.flush()
        utags = [i for i in a.utags.split(",") if i != ""]
        if tag_id not in utags:
            utags.append(str(tag_id))
            utags = list(set(utags))
            a.utags = "," + ",".join(utags) + ","
    db.session.commit()
    session["notice"] = "标签添加成功"
    return redirect(url_for("Index.index"))
