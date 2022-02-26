from flask import session

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