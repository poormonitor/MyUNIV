from typing import List, Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session, aliased
from sqlalchemy import and_, or_, func

from misc.func import freezeDict, hash_dict, lru_cache_ignored
from misc.model import QueryResult, parse_result
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
    standard: int
    accordation: Optional[bool] = False
    page: int = 1


@router.post("")
def query(form: QueryForm, db: Session = Depends(get_db)):
    count, result = findResult(freezeDict(form.dict()), db)
    return QueryResult(total=count, result=parse_result(result))


@hash_dict
@lru_cache_ignored(64)
def findResult(info, db):
    from models.conne import Conne
    from models.major import Major
    from models.must import Must
    from models.rank import Rank
    from models.univ import Univ

    MustS = db.query(Must)
    RankS = db.query(Rank)
    UnivS = db.query(Univ)
    MajorS = db.query(Major)

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
            RankS = RankS.filter(Rank.rank >= rank)
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
    result = result.join(Conne, Conne.mid == RankAlias.mid)
    result = result.join(MustAlias, Conne.mmid == MustAlias.mmid)

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

    if info["mymust"]:
        if info["accordation"]:
            result = result.order_by(MustAlias.must)
        else:
            result = result.order_by(MustAlias.must.desc())

    if info["rank"]:
        if not info["rank_range"]:
            result = result.order_by(RankAlias.rank.asc())
        else:
            result = result.order_by(func.abs(RankAlias.rank - info["rank"]).asc())
    else:
        result = result.order_by(UnivAlias.sid.asc())

    result = result.group_by(MajorAlias.mid)

    count = result.count()

    if info["page"]:
        result = result.offset((info["page"] - 1) * 50).limit(50).all()
    else:
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