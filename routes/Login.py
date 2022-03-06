from models.User import User
from flask import Blueprint, render_template, request, session, redirect, url_for
from models import db
from hashlib import md5

login_bp = Blueprint('Login', __name__)


@login_bp.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        import os
        session["nonce"] = os.urandom(16).hex()
        session["csrf"] = os.urandom(16).hex()
        error = request.args.get('error', None)
        error = {
            "1": "密码错误",
            "2": "参数错误",
            "3": "账号不存在"
        }[error] if error else None
        return render_template('login.html',
                               csrf=session["csrf"],
                               nonce=session["nonce"],
                               error=error)
    uid = request.form['uid']
    passwd = request.form['passwd']
    csrf = request.form['csrf']
    nonce = session["nonce"]
    result = User.query.filter_by(uid=uid).first()
    if not result:
        return redirect(url_for('Login.login', error=3))
    if md5(str(result.passwd + nonce).encode("utf-8")).hexdigest() != passwd:
        return redirect(url_for('Login.login', error=1))
    if csrf != session["csrf"]:
        return redirect(url_for('Login.login', error=2))
    session["uid"] = uid
    session["name"] = result.name
    session["admin"] = result.admin
    session["must"] = result.must
    # update last login
    result.last_login = db.func.now()
    return redirect(url_for('Index.index'))


@login_bp.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('Index.index'))