from flask import session, request, redirect, url_for
from functools import wraps


def islogin():
    if "uid" in session:
        return True
    else:
        return False


def isadmin():
    return True
    if islogin() and session["admin"] == True:
        return True
    else:
        return False


def valid_csrf():
    if "csrf" in session and session["csrf"] == request.form["csrf"]:
        return True
    else:
        return False


def login_required(f):

    @wraps(f)
    def wrap(*args, **kwargs):
        if islogin():
            return f(*args, **kwargs)
        else:
            return redirect(url_for('Login.login'))

    return wrap


def admin_required(f):

    @wraps(f)
    def wrap(*args, **kwargs):
        if not islogin():
            return redirect(url_for('Login.login'))
        elif not isadmin():
            return redirect(url_for('Index.Index'))
        else:
            return f(*args, **kwargs)

    return wrap