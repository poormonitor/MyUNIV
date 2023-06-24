from functools import lru_cache, wraps


def isPatString(needle, haystack):
    for i in needle:
        if i in haystack:
            return i
    return None


def isSuborPatString(needle, haystack):
    for i in haystack:
        if needle in i or i in needle:
            return True
    return False


def get_school_name(name: str):
    import re

    from misc.const import allow_tags

    tags = []
    univ_name = name.split("(")[0]
    tag = re.findall(r"(?<=[\(]).*?(?=[\)])", name)
    for j in tag:
        if j not in allow_tags and not isSuborPatString(j, allow_tags):
            univ_name += "(" + j + ")"
        else:
            tags.append(j)
    return univ_name, tags


def get_must_string(now: int) -> str:
    from misc.const import majors

    if not now:
        return majors[0]
    now = str(now)
    cnt = now[0]
    ans = []
    for i in now[1:]:
        ans.append(majors[int(i)])
    return ", ".join(ans) + " " + "(必选%d门)" % int(cnt)


def get_mymust_string(now: int) -> str:
    from misc.const import majors

    if not now:
        return ""
    now = str(now)
    ans = []
    for i in now:
        ans.append(majors[int(i)])
    return ", ".join(ans)


def lru_cache_ignored(*args, **kwargs):
    lru_decorator = lru_cache(*args, **kwargs)

    class _Equals(object):
        def __init__(self, o):
            self.obj = o

        def __eq__(self, other):
            return True

        def __hash__(self):
            return 0

    def decorator(f):
        @lru_decorator
        def helper(arg1, *args, **kwargs):
            args = map(lambda x: x.obj, args)
            return f(arg1, *args, **kwargs)

        @wraps(f)
        def function(arg1, *args, **kwargs):
            args = map(_Equals, args)
            return helper(arg1, *args, **kwargs)

        return function

    return decorator


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


@lru_cache(256)
def findNearestMust(major, year):
    from models.must import Must

    allMust = Must.query.filter(Must.year == year).all()
    result = findNearestMustInAll(major, allMust)
    return result


def process_excel(xlsx, year, delete=False):
    import os

    from pandas import read_excel
    from tqdm import tqdm

    from misc.const import majors, provinces, rqs
    from models import get_db
    from models.major import Major
    from models.must import Must
    from models.rank import Rank
    from models.tag import Tag
    from models.univ import Univ

    db = list(get_db())[0]
    data = read_excel(xlsx)
    if "位次" in data.columns.tolist():
        univs = {i.uname: [i.sid, i.utags] for i in db.query(Univ).all()}
        tags = {i.tname: i.tid for i in db.query(Tag).all()}
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
                        db.add(t)
                        db.flush()
                        tid = t.tid
                        tags[j] = tid
                    else:
                        tid = tags[j]
                    tids.append(tid)
                tids = "," + ",".join(str(i) for i in sorted(tids)) + ","
                univ = Univ(uname=univ_name, utags=tids, province=0)
                db.add(univ)
                db.flush()
                univs[univ_name] = [univ.sid, univ.utags]
            elif (
                "," + ",".join(str(tags.get(i, -1)) for i in tag) + ","
                != univs[univ_name][1]
            ):
                tids = []
                for j in tag:
                    if j not in tags:
                        t = Tag(tname=j)
                        db.add(t)
                        db.flush()
                        tid = t.tid
                        tags[j] = tid
                    else:
                        tid = tags[j]
                    tids.append(tid)
                tids = "," + ",".join(str(i) for i in sorted(tids)) + ","
                univ = db.query(Univ).filter_by(sid=univs[univ_name][0]).first()
                univ.utags = tids
                db.flush()

            univ_id = univs[univ_name][0]

            if (
                b := db.query(Major).filter_by(sid=univ_id, mname=major).first()
            ) is None:
                b = Major(sid=univ_id, mname=major)
                db.add(b)
                db.flush()

            if (
                a := db.query(Rank).filter(Rank.mid == b.mid, Rank.year == year).first()
            ) is None:
                rank = Rank(
                    mid=b.mid, year=year, rank=rank, schedule=schedule, score=score
                )
                db.add(rank)
                db.flush()
            else:
                a.rank = rank
                a.schedule = schedule
                a.score = score
                db.flush()

    elif "选考科目要求" in data.columns.tolist():
        univs = {i.uname: [i.sid, i.province] for i in db.query(Univ).all()}
        for i in tqdm(data.values):
            province = i[0]
            univ_name = unifyBracket(i[1])
            univ_name, _ = get_school_name(univ_name)
            major = unifyBracket(i[2])
            include = unifyBracket(i[3]) if i[3] == i[3] else ""
            must = int(
                "".join(
                    sorted(
                        [str(majors.index(j)) for j in i[5].split("(")[0].split(",")]
                    )
                )
            )

            if must != 0:
                if rs := isPatString(i[5], rqs.keys()):
                    must = int(rqs[rs] + str(must))
                else:
                    must = int(str(len(str(must))) + str(must))

            province_id = list(provinces.keys())[
                list(provinces.values()).index(province)
            ]

            if univ_name not in univs:
                univ = Univ(uname=univ_name, province=province_id)
                db.add(univ)
                db.flush()
                univs[univ_name] = [univ.sid, univ.province]
            elif univs[univ_name][1] != province:
                univ = db.query(Univ).filter(Univ.uname == univ_name).first()
                univ.province = province_id
                db.flush()
                univs[univ_name][1] = province_id

            univ_id = univs[univ_name][0]

            if (
                a := db.query(Must)
                .filter_by(mname=major, sid=univ_id, year=year)
                .first()
            ) is None:
                must = Must(
                    mname=major, year=year, sid=univ_id, must=must, include=include
                )
                db.add(must)
            else:
                a.must = must
                a.include = include
            db.flush()

    if delete:
        os.remove(xlsx)
    db.commit()


def stringSim(a, b):
    if not a or not b:
        return 0

    from Levenshtein import jaro_winkler as ratio

    return ratio(a, b)


def findNearestMustInAll(name, sequence):
    m = -1
    res = None
    for i in sequence:
        temp = max(
            [stringSim(name, i.mname)]
            + [stringSim(name, j) for j in i.include.split("、")]
        )
        if temp > m:
            m = temp
            res = i
    return res, m


def findNearestMustInAllSchool(name, sequence):
    res = None
    temp = -1
    for i in sequence:
        tmp = max(
            [stringSim(name, i.mname)]
            + [stringSim(name, j) for j in i.include.split("、")]
        )
        if tmp > 0.9:
            return i
        elif tmp > temp:
            temp = tmp
            res = i
    return res


def connectMust():
    from itertools import groupby

    from sqlalchemy import func
    from tqdm import tqdm

    from models import get_db
    from models.conne import Conne
    from models.major import Major
    from models.must import Must
    from models.rank import Rank

    db = list(get_db())[0]
    allMajor = db.query(Major).all()
    allMust = db.query(Must).all()
    schoolRank = (
        db.query(Major.sid, func.avg(Rank.score))
        .outerjoin(Major, Major.mid == Rank.mid)
        .group_by(Major.sid)
        .order_by(func.avg(Rank.score))
        .all()
    )
    schoolRank = {i[0]: i[1] for i in schoolRank}

    allMustByYear = {i: [k for k in j] for i, j in groupby(allMust, lambda x: x.year)}
    allMustByYearSchool = {
        i: {k: [l for l in m] for k, m in groupby(j, lambda x: x.sid)}
        for i, j in allMustByYear.items()
    }

    scoreAvgBySchool = {
        i[0]: [(j[1], i[1].get(j[0])) for j in schoolRank.items()]
        for i in allMustByYearSchool.items()
    }

    must_years = list(allMustByYear.keys())

    for i in tqdm(allMajor):
        for j in must_years:
            res, tmp = findNearestMustInAll(
                i.mname, allMustByYearSchool.get(j, {}).get(i.sid, [])
            )
            if not res or tmp < 0.4:
                ordered = sorted(
                    scoreAvgBySchool.get(j, []),
                    key=lambda x: abs(x[0] - schoolRank[i.sid]),
                )
                res = findNearestMustInAllSchool(
                    i.mname, [j for k in ordered if k[1] for j in k[1]]
                )
            if not res:
                continue
            if (a := db.query(Conne).filter_by(mid=i.mid, year=j).first()) is None:
                conn = Conne(i.mid, res.mmid, j)
                db.add(conn)
            elif a.mmid != res.mmid:
                a.mmid = res.mmid
    db.commit()


def cleanAll():
    from models import get_db
    from models.conne import Conne
    from models.major import Major
    from models.must import Must
    from models.rank import Rank
    from models.univ import Univ
    from models.tag import Tag

    db = list(get_db())[0]

    db.query(Univ).delete()
    db.query(Major).delete()
    db.query(Must).delete()
    db.query(Rank).delete()
    db.query(Conne).delete()
    db.query(Tag).delete()
    db.commit()

    return True


def datetime_to_str(date_time):
    if not date_time:
        return ""

    from pytz import timezone

    tz = timezone("Asia/Shanghai")
    utc = timezone("UTC")

    return date_time.replace(tzinfo=utc).astimezone(tz).strftime("%Y-%m-%d %H:%M:%S")
