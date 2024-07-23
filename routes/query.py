from typing import List, Optional, Tuple

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session, aliased
from sqlalchemy import and_, or_

from misc.func import (
    freezeDict,
    hash_dict,
    lru_cache_ignored,
    get_school_name,
    unifyBracket,
)
from misc.model import QueryResult, parse_result, QueryResultMini, parse_result_mini
from models import get_db

router = APIRouter()


class QueryForm(BaseModel):
    rank: Optional[int] = None
    year: int
    school: Optional[str] = None
    major: Optional[str] = None
    rank_range: Optional[int] = None
    utags: Optional[str] = None
    province: Optional[List[int]] = []
    utags: Optional[List[int]] = []
    nutags: Optional[List[int]] = []
    mymust: Optional[List[int]] = []
    batch: Optional[int] = 0
    standard: int
    accordation: Optional[bool] = False
    page: int = 1
    page_size: int = 50


@router.post("")
def query(form: QueryForm, db: Session = Depends(get_db)):
    count, result = findResult(freezeDict(form.dict()), db)
    return QueryResult(total=count, result=parse_result(result))


@hash_dict
@lru_cache_ignored(64, count=1)
def findResult(info, db):
    from models.conne import Conne
    from models.major import Major
    from models.must import Must
    from models.rank import Rank
    from models.univ import Univ

    RankS = db.query(Rank)
    UnivS = db.query(Univ)
    MajorS = db.query(Major)
    MustS = db.query(Must, Conne.mid)
    MustS = MustS.join(Conne, Conne.mmid == Must.mmid)

    if info["batch"]:
        MajorS = MajorS.filter(Major.batch == info["batch"])

    MustS = MustS.filter(Must.year == info["standard"])
    if info["mymust"]:
        mymust = "".join(map(str, info["mymust"]))
        if info["accordation"]:
            what_i_can = get_what_i_can_choose_most(mymust)
        else:
            what_i_can = get_what_i_can_choose(mymust)
        MustS = MustS.filter(Must.must.in_(what_i_can))

    RankS = RankS.filter(Rank.year == info["year"])
    if info["rank"]:
        rank = info["rank"]
        if not info["rank_range"]:
            if info["rank"] <= 4000:
                RankS = RankS.filter(Rank.rank <= info["rank"] + 700)
                RankS = RankS.filter(Rank.rank >= info["rank"] - 700)
            elif info["rank"] <= 20000:
                RankS = RankS.filter(Rank.rank >= rank * 0.8)
                RankS = RankS.filter(Rank.rank <= rank * 1.2)
            else:
                RankS = RankS.filter(Rank.rank >= info["rank"] - 7000)
                RankS = RankS.filter(Rank.rank <= info["rank"] + 7000)
        else:
            RankS = RankS.filter(Rank.rank >= rank - info["rank_range"])
            RankS = RankS.filter(Rank.rank <= rank + info["rank_range"])

        RankS = RankS.filter(Rank.rank != 0)

    if info["school"]:
        for i in info["school"].split(" "):
            UnivS = UnivS.filter(Univ.uname.like("%" + i + "%"))

    if info["utags"]:
        for i in info["utags"]:
            UnivS = UnivS.filter(Univ.utags.like("%," + str(i) + ",%"))

    if info["nutags"]:
        for i in info["nutags"]:
            UnivS = UnivS.filter(Univ.utags.notlike("%," + str(i) + ",%"))

    if info["province"]:
        UnivS = UnivS.filter(Univ.province.in_(info["province"]))

    datas = ["mymust", "school", "utags", "nutags", "province", "major", "batch"]
    filtered = any([info[i] for i in datas])
    if not filtered:
        count = RankS.count()

        if info["rank"]:
            RankS = RankS.order_by(Rank.rank.asc())
        else:
            RankS = RankS.order_by(Rank.rmid.asc())

        page_size = info["page_size"]
        RankS = RankS.offset((info["page"] - 1) * page_size).limit(page_size)

    RankS = RankS.subquery()
    RankAlias = aliased(Rank, RankS)
    UnivS = UnivS.subquery()
    UnivAlias = aliased(Univ, UnivS)
    MajorS = MajorS.subquery()
    MajorAlias = aliased(Major, MajorS)
    MustS = MustS.subquery()
    MustAlias = aliased(Must, MustS)

    result = db.query(MajorAlias, UnivAlias, RankAlias, MustAlias)
    result = result.select_from(RankAlias)
    result = result.join(MajorAlias, MajorAlias.mid == RankAlias.mid)
    result = result.join(UnivAlias, UnivAlias.sid == MajorAlias.sid)
    result = result.join(MustAlias, MustS.c.mid == MajorAlias.mid)

    if info["major"]:
        for i in info["major"].split():
            result = result.filter(
                or_(
                    MajorAlias.mname.contains(i),
                    and_(
                        MustAlias.include.contains(i),
                        MustAlias.mname.contains(MajorAlias.mname),
                    ),
                )
            )

    if info["mymust"] and info["accordation"]:
        result = result.order_by(MustAlias.must.desc())

    if filtered or info["rank"] is not None:
        result = result.order_by(RankAlias.rank == 0)
        result = result.order_by(RankAlias.rank.asc())
    else:
        result = result.order_by(RankAlias.rmid.asc())

    result = result.group_by(MajorAlias.mid)

    if filtered:
        count = result.count()

        page_size = info["page_size"]
        result = result.offset((info["page"] - 1) * page_size).limit(page_size)

    result = result.all()

    db.expunge_all()

    return count, result


def get_what_i_can_choose(mymust: str) -> list:
    from itertools import combinations

    choices = [i for i in range(1, 8)]
    musts = list(map(int, list(mymust)))
    ans = ["0"]
    # Perfectly matched
    for i in range(1, len(musts) + 1):
        for j in combinations(musts, i):
            ans.append(str(i) + "".join(map(str, j)))
    # With redundancy
    for i in range(1, 4):
        for j in range(1, 4 - i):
            for k in combinations(musts, i):
                new_choice = choices[:]
                for p in k:
                    new_choice.remove(p)
                for l in combinations(new_choice, j):
                    ans.append(str(i) + "".join(map(str, sorted(k + l))))
    return sorted(list(set(ans)))


def get_what_i_can_choose_most(mymust: str) -> list:
    from itertools import combinations

    choices = [i for i in range(1, 8)]
    musts = list(map(int, list(mymust)))
    ans = []
    # Perfectly matched
    for i in range((len(musts) + 1) // 2, len(musts) + 1):
        for j in combinations(musts, i):
            ans.append(str(i) + "".join(map(str, j)))
    # With redundancy
    for i in range((len(musts) + 1) // 2, len(musts) + 1):
        for j in range(1, 4 - i):
            for k in combinations(musts, i):
                new_choice = choices[:]
                for p in k:
                    new_choice.remove(p)
                for l in combinations(new_choice, j):
                    ans.append(str(i) + "".join(map(str, sorted(k + l))))
    return ans


@lru_cache_ignored(64, count=3)
def get_rank(school: str, major: str, year: int, db: Session) -> Tuple[int, int, int]:
    from models.rank import Rank
    from models.major import Major
    from models.univ import Univ

    univ = db.query(Univ).filter(Univ.uname == school).first()
    major = db.query(Major).filter(Major.mname == major, Major.sid == univ.sid).first()

    if not univ or not major:
        return None

    rank = db.query(Rank).filter(Rank.mid == major.mid, Rank.year == year).first()

    if not rank:
        return None

    db.expunge_all()

    return major, univ, rank


class QueryRankForm(BaseModel):
    uname: str
    mname: str


class QueryRanksForm(BaseModel):
    list: List[QueryRankForm]
    year: int


@router.post("/ranks")
def query_ranks(form: QueryRanksForm, db: Session = Depends(get_db)):
    result = []

    for i in form.list:
        uname = unifyBracket(i.uname)
        uname = get_school_name(uname)[0]
        uname = uname[uname.find(" ") + 1 :]

        mname = unifyBracket(i.mname)
        mname = mname[mname.find(" ") + 1 :]
        mname = mname[: mname.rfind("(")]

        info = get_rank(uname, mname, form.year, db)
        if info:
            result.append(info)

    result = QueryResultMini(result=parse_result_mini(result))
    return result
