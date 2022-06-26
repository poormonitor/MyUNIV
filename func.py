from flask import session, request, redirect, url_for
from functools import wraps, lru_cache


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
    if (
        "csrf" in session
        and "csrf" in request.form
        and session["csrf"] == request.form["csrf"]
    ):
        return True
    else:
        return False


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if islogin():
            return f(*args, **kwargs)
        else:
            session["referer"] = (request.endpoint, request.view_args)
            return redirect(url_for("Login.login"))

    return wrap


def not_login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if islogin():
            return redirect(url_for("Login.logout"))
        else:
            return f(*args, **kwargs)

    return wrap


def login_required_ajax(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if islogin():
            return f(*args, **kwargs)
        else:
            return "not logged in"

    return wrap


def admin_required_ajax(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if not islogin():
            return "not logged in"
        elif not isadmin():
            return "not admin"
        else:
            return f(*args, **kwargs)

    return wrap


def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if not islogin():
            return redirect(url_for("Login.login"))
        elif not isadmin():
            return redirect(url_for("Index.index"))
        else:
            return f(*args, **kwargs)

    return wrap


def csrf_valid_if_post(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if request.method != "POST" or valid_csrf():
            return f(*args, **kwargs)
        return redirect(url_for("Index.index"))

    return wrap


def csrf_valid(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if valid_csrf():
            return f(*args, **kwargs)
        return redirect(url_for("Index.index"))

    return wrap


def get_school_name(name: str):
    import re
    from const import allow_tags

    tags = []
    univ_name = name.split("(")[0]
    tag = re.findall(r"(?<=[\(]).*?(?=[\)])", name)
    for j in tag:
        if j not in allow_tags:
            univ_name += "(" + j + ")"
        else:
            tags.append(j)
    return univ_name, tags


def get_what_i_can_choose(mymust: str) -> list:
    from itertools import combinations

    choices = [i for i in range(1, 8)]
    musts = list(map(int, list(mymust)))
    ans = ["0"]
    for i in range(1, len(musts) + 1):
        for j in combinations(musts, i):
            new_choice = choices[:]
            for p in j:
                new_choice.remove(p)
            for p in combinations(new_choice, i - len(j)):
                ans.append(str(i) + "".join(map(str, j + p)))
    return ans


def get_what_i_can_choose_most(mymust: str) -> list:
    from itertools import combinations

    choices = [i for i in range(1, 8)]
    musts = list(map(int, list(mymust)))
    ans = []
    for i in range((len(musts) + 1) // 2, len(musts) + 1):
        for j in combinations(musts, i):
            new_choice = choices[:]
            for p in j:
                new_choice.remove(p)
            for p in combinations(new_choice, i - len(j)):
                ans.append(str(i) + "".join(map(str, j + p)))
    return ans


def get_must_string(now: int) -> str:
    from const import majors

    if not now:
        return majors[0]
    now = str(now)
    cnt = now[0]
    ans = []
    for i in now[1:]:
        ans.append(majors[int(i)])
    return ", ".join(ans) + " " + "(必选%d门)" % int(cnt)


def get_mymust_string(now: int) -> str:
    from const import majors

    if not now:
        return ""
    now = str(now)
    ans = []
    for i in now:
        ans.append(majors[int(i)])
    return ", ".join(ans)


def hash_dict(func):
    """Transform mutable dictionnary
    Into immutable
    Useful to be compatible with cache
    """

    class HDict(dict):
        def __hash__(self):
            return hash(frozenset(self.items()))

    @wraps(func)
    def wrapped(*args, **kwargs):
        args = tuple([HDict(arg) if isinstance(arg, dict) else arg for arg in args])
        kwargs = {k: HDict(v) if isinstance(v, dict) else v for k, v in kwargs.items()}
        return func(*args, **kwargs)

    return wrapped


def freezeDict(dict):
    return {i[0]: tuple(i[1]) if isinstance(i[1], list) else i[1] for i in dict.items()}


def unifyBracket(st):
    return st.replace("（", "(").replace("）", ")")


def findNearestMust(major, year):
    from models.Must import Must
    from models.Major import Major
    from models import db

    result = db.session.query(Must, Major)
    result = result.outerjoin(Must, Must.sid == Major.sid)
    result = result.filter(Major.mid == int(major.mid))
    result = result.filter(
        db.or_(
            Major.mname == Must.mname,
            Major.mname.contains(Must.mname),
            Must.mname.contains(Major.mname),
            Must.include.contains(Major.mname),
        )
    )
    result = result.order_by(db.func.abs(Must.year - year).asc())
    result = result.order_by(db.func.length(Must.mname).desc())
    result = result.first()
    return result[0] if result else None


@hash_dict
@lru_cache(512)
def findResult(page, info):
    from models.Major import Major
    from models.Univ import Univ
    from models.Rank import Rank
    from models.Conne import Conne
    from models.Must import Must
    from models import db

    result = db.session.query(Major, Univ, Rank, Must, Conne)
    result = result.select_from(Rank)
    result = result.outerjoin(Major, Major.mid == Rank.mid)
    result = result.outerjoin(Univ, Univ.sid == Major.sid)
    result = result.outerjoin(Conne, Conne.mid == Rank.mid)
    result = result.outerjoin(
        Must, db.and_(Conne.mmid == Must.mmid, Conne.year == Must.year)
    )

    if info["school"]:
        for i in info["school"].split(" "):
            result = result.filter(Univ.uname.like("%" + i + "%"))

    if info["major"]:
        result = result.filter(Major.mname.like("%" + info["major"] + "%"))

    result = result.filter(Rank.year == info["year"])

    if info["rank"]:
        rank = info["rank"]
        if not info["rank_range"]:
            result = result.filter(Rank.rank >= rank).filter(Rank.rank != 0)
            result = result.order_by(Rank.rank.asc())
        else:
            result = result.filter(
                rank - info["rank_range"] <= Rank.rank,
                Rank.rank <= rank + info["rank_range"],
            ).filter(Rank.rank != 0)
            result = result.order_by(db.func.abs(Rank.rank - rank).asc())
    else:
        result = result.order_by(Univ.sid.asc())

    if info["mymust"]:
        mymust = "".join(map(str, info["mymust"]))
        result = result.order_by(Must.must.desc())
        if info["accordation"]:
            what_i_can = get_what_i_can_choose_most(mymust)
        else:
            what_i_can = get_what_i_can_choose(mymust)
        result = result.filter(Must.must.in_(what_i_can))

    result = result.filter(Must.year == info["standard"])
    result = result.group_by(Major.mid)

    if info["utags"]:
        condition = db.or_(Univ.utags.like("%," + str(i) + ",%") for i in info["utags"])
        result = result.filter(condition)

    if info["nutags"]:
        ncondition = db.not_(
            db.and_(Univ.utags.like("%," + str(i) + ",%") for i in info["nutags"])
        )
        result = result.filter(ncondition)

    if info["province"]:
        result = result.filter(Univ.province.in_(info["province"]))

    if info["sort"]:
        result = result.filter(
            db.or_(Must.include.contains(i) for i in info["sort"].split(" "))
        )

    count = result.count()

    if page:
        result = result.offset((page - 1) * 50).limit(50).all()
    else:
        result = result.all()

    result = [
        i if i[3] else (i[0], i[1], i[2], findNearestMust(i[0], info["standard"]))
        for i in result
    ]

    db.session.expunge_all()

    return count, result


def process_excel(xlsx, year, delete=False):
    from models import db
    from models.Major import Major
    from models.Univ import Univ
    from models.Must import Must
    from models.Tag import Tag
    from models.Rank import Rank
    from pandas import read_excel
    from const import provinces, majors
    from func import get_school_name, unifyBracket
    from tqdm import tqdm
    import os
    import re

    data = read_excel(xlsx)
    if "位次" in data.columns.tolist():
        univs = {i.uname: [i.sid, i.utags] for i in Univ.query.all()}
        tags = {i.tname: i.tid for i in Tag.query.all()}
        for i in tqdm(data.values):
            univ_name = unifyBracket(i[1])
            univ_name, tag = get_school_name(univ_name)
            major = unifyBracket(i[3])
            schedule = i[4]
            score = i[5]
            rank = i[6] if i[6] == i[6] else 0
            if univ_name not in univs:
                tids = []
                for j in tag:
                    if j not in tags:
                        t = Tag(tname=j)
                        db.session.add(t)
                        db.session.flush()
                        tid = t.tid
                        tags[j] = tid
                    else:
                        tid = tags[j]
                    tids.append(tid)
                tids = "," + ",".join(str(i) for i in sorted(tids)) + ","
                univ = Univ(uname=univ_name, utags=tids, province=0)
                db.session.add(univ)
                db.session.flush()
                univs[univ_name] = [univ.sid, univ.utags]
            elif (
                "," + ",".join(str(tags.get(i, -1)) for i in tag) + ","
                != univs[univ_name][1]
            ):
                tids = []
                for j in tag:
                    if j not in tags:
                        t = Tag(tname=j)
                        db.session.add(t)
                        db.session.flush()
                        tid = t.tid
                        tags[j] = tid
                    else:
                        tid = tags[j]
                    tids.append(tid)
                tids = "," + ",".join(str(i) for i in sorted(tids)) + ","
                univ = Univ.query.filter_by(sid=univs[univ_name][0]).first()
                univ.utags = tids
                db.session.flush()

            univ_id = univs[univ_name][0]

            if (b := Major.query.filter_by(sid=univ_id, mname=major).first()) is None:
                b = Major(sid=univ_id, mname=major)
                db.session.add(b)
                db.session.flush()

            if (
                a := db.session.query(Rank)
                .filter(Rank.mid == b.mid, Rank.year == year)
                .first()
            ) is None:
                db.session.add(
                    Rank(
                        mid=b.mid, year=year, rank=rank, schedule=schedule, score=score
                    )
                )
                db.session.flush()
            else:
                a.rank = rank
                a.schedule = schedule
                a.score = score
                db.session.flush()

    elif "选考科目要求" in data.columns.tolist():
        univs = {i.uname: [i.sid, i.province] for i in Univ.query.all()}
        for i in tqdm(data.values):
            province = i[0]
            univ_name = unifyBracket(i[1])
            univ_name, _ = get_school_name(univ_name)
            major = unifyBracket(i[2])
            include = unifyBracket(i[3]) if i[3] == i[3] else ""
            must = int(
                "".join([str(majors.index(j)) for j in i[5].split("(")[0].split(",")])
            )
            if must != 0:
                must = int(re.search(r"\d+", i[5]).group(0) + str(must))
            province_id = list(provinces.keys())[
                list(provinces.values()).index(province)
            ]

            if univ_name not in univs:
                univ = Univ(uname=univ_name, province=province_id)
                db.session.add(univ)
                db.session.flush()
                univs[univ_name] = [univ.sid, univ.province]
            elif univs[univ_name][1] != province:
                univ = db.session.query(Univ).filter(Univ.uname == univ_name).first()
                univ.province = province_id
                db.session.flush()
                univs[univ_name][1] = province_id

            univ_id = univs[univ_name][0]

            if (
                a := Must.query.filter_by(mname=major, sid=univ_id, year=year).first()
            ) is None:
                db.session.add(
                    Must(
                        mname=major, year=year, sid=univ_id, must=must, include=include
                    )
                )
            else:
                a.must = must
                a.include = include
            db.session.flush()

    if delete:
        os.remove(xlsx)
    db.session.commit()


def subString(needle, sequence):
    for i in sequence:
        if needle in i or i in needle:
            return True
    return False


def stringSim(a, b):
    from difflib import SequenceMatcher

    return SequenceMatcher(None, a, b).quick_ratio()


def findNearestMustInAll(name, sequence):
    m = -1
    res = None
    for i in sequence:
        temp = max(
            [stringSim(name, i.mname)]
            + [stringSim(name, j) for j in i.include.split("、")]
        )
        if subString(name, [i.mname] + list(i.include.split("、"))):
            temp += 1
        if temp > m:
            m = temp
            res = i
    return res


def findNearestMustInAllSchool(name, sequence):
    for i in sequence:
        temp = max(
            [stringSim(name, i.mname)]
            + [stringSim(name, j) for j in i.include.split("、")]
        )
        if temp > 0.9:
            return i
    return None


def connectMust():
    from models.Conne import Conne
    from models.Major import Major
    from models.Must import Must
    from models import db
    from tqdm import tqdm
    from itertools import groupby

    allMajor = Major.query.all()
    allMust = Must.query.all()
    allMustByYear = {i: [k for k in j] for i, j in groupby(allMust, lambda x: x.year)}
    allMustByYearSchool = {
        i: {k: [l for l in m] for k, m in groupby(j, lambda x: x.sid)}
        for i, j in allMustByYear.items()
    }
    must_years = list(allMustByYear.keys())
    for i in tqdm(allMajor):
        for j in must_years:
            res = findNearestMustInAll(
                i.mname, allMustByYearSchool.get(j, {}).get(i.sid, [])
            )
            if not res:
                res = findNearestMustInAllSchool(i.mname, allMustByYear.get(j, []))
            if not res:
                continue
            if (a := Conne.query.filter_by(mid=i.mid, year=j).first()) is None:
                conn = Conne(i.mid, res.mmid, j)
                db.session.add(conn)
            elif a.mmid != res.mmid:
                a.mmid = res.mmid
    db.session.commit()
