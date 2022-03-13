from flask import Blueprint, redirect, render_template, session, request, url_for
from func import admin_required, valid_csrf
from models import db
from models.User import User
from hashlib import md5
import re
import os

add_user_bp = Blueprint('AddUser', __name__)


@add_user_bp.route('/adduser', methods=['GET', 'POST'])
@admin_required
def adduser():
    if request.method == "GET":
        session['csrf'] = os.urandom(16).hex()
        return render_template('adduser.html', csrf=session["csrf"])
    if not valid_csrf():
        return redirect(url_for('AddUser.adduser'))
    users = request.form.get("users")
    tp = int(request.form.get("type"))
    for line in users.splitlines():
        items = re.split(",| |\t", line)
        if (a := User.query.filter_by(uid=items[0]).first()) is None:
            passwd = md5(str(items[2]).encode("utf-8")).hexdigest()
            db.session.add(
                User(uid=items[0],
                     name=items[1],
                     password=passwd,
                     admin=True if tp else False))
        else:
            passwd = md5(str(items[2]).encode("utf-8")).hexdigest()
            a.password = passwd
            a.name = items[1]
            a.admin = True if tp else False
    db.session.commit()
    return redirect(url_for('AddUser.adduser'))
