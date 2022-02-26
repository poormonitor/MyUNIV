def islogin():
    global session
    if 'uid' in session:
        return True
    else:
        return False


def isadmin():
    global session
    from models import db, User
    if islogin() and db.session.query(
            db.session.query(User).filter(
                User.id == session['userid']).first().isadmin).first() == True:
        return True
    else:
        return False