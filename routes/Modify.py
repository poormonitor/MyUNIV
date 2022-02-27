from flask import Blueprint, redirect, render_template, session, request, url_for
from func import islogin, valid_csrf
from models import db
from models.User import User
import os

modify_bp = Blueprint('Modify', __name__)


@modify_bp.route('/modify', methods=['GET', 'POST'])
def modify():
    if islogin():
        result = User.query.filter_by(uid=session['uid']).first()
        if request.method == "GET":
            error = None
            if "error" in request.args:
                error = {"1": "原密码错误"}[request.args["error"]]
            session['csrf'] = os.urandom(16).hex()
            return render_template('modify.html',
                                   session=session,
                                   csrf=session["csrf"],
                                   error=error,
                                   result=result)
        if not valid_csrf():
            return redirect(url_for('Modify.modify'))
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        if result.passwd != old_password:
            return redirect(url_for('Modify.modify', error="1"))
        result.passwd = new_password
        db.session.commit()
    return redirect(url_for('Index.index'))
