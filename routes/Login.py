from models.User import User
from flask import Blueprint, render_template, request, abort, session, redirect
from hashlib import md5

login_bp = Blueprint('Login', __name__)


@login_bp.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        import os
        session["nonce"] = os.urandom(16).hex()
        session["csrf"] = os.urandom(16).hex()
        error = request.args.get('error', None)
        error = {"1": "密码错误", "2": "参数错误"}[error] if error else None
        return render_template('login.html',
                               session=session,
                               csrf=session["csrf"],
                               nonce=session["nonce"],
                               error=error)
    try:
        uid = request.form['uid']
        passwd = request.form['passwd']
        csrf = request.form['csrf']
        nonce = session["nonce"]
    except KeyError:
        abort(400)
    result = User.query.filter_by(uid=uid).first()
    print(result)
    if md5(result.passwd + nonce) != passwd:
        return redirect('/login?error=1')
    if csrf != session["csrf"]:
        return redirect('/login?error=2')
    session["uid"] = uid
    session["name"] = result.name
    session["admin"] = result.admin
    session["must"] = result.must
    return redirect('/')
