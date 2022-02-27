from flask import session, request


def islogin():
    if "uid" in session:
        return True
    else:
        return False


def isadmin():
    if islogin() and session["admin"] == True:
        return True
    else:
        return False


def valid_csrf():
    if "csrf" in session and session["csrf"] == request.form["csrf"]:
        return True
    else:
        return False