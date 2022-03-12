from flask import session, request, redirect, url_for
from functools import wraps
from typing import List


def islogin():
    return True
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


def get_school_name(name: str):
    import re
    from const import allow_tags
    univ_name = name.split("(")[0]
    tag = re.findall(r'(?<=[\(]).*?(?=[\)])', univ_name)
    for j in tag:
        if j not in allow_tags:
            univ_name += "(" + j + ")"
    return univ_name


def get_what_i_can_choose(mymust: str) -> List[str]:
    from itertools import combinations
    choices = [i for i in range(1, 8)]
    musts = list(map(int, list(mymust)))
    ans = combinations(choices, 3)
    ans = list(map(lambda x: "0" + str("".join(map(str, x))), ans))
    for i in range(1, 3):
        for j in combinations(musts, i):
            print(j)
            new_choice = choices[:]
            for p in j:
                new_choice.remove(p)
            for p in combinations(new_choice, i - len(j)):
                print(p)
                print(j)
                ans.append(str(i) + "".join(map(str, j + p)))
    ans.append("3" + str(mymust))
    return ans
