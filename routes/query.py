from typing import List, Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, not_, func

from misc.func import findNearestMust, freezeDict, hash_dict, lru_cache_ignored
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

    result = db.query(Major, Univ, Rank, Must)
    result = result.select_from(Rank)
    result = result.outerjoin(Major, Major.mid == Rank.mid)
    result = result.outerjoin(Univ, Univ.sid == Major.sid)
    result = result.outerjoin(Conne, Conne.mid == Rank.mid)
    result = result.outerjoin(
        Must, and_(Conne.mmid == Must.mmid, Conne.year == Must.year)
    )

    if info["school"]:
        for i in info["school"].split(" "):
            result = result.filter(Univ.uname.like("%" + i + "%"))

    if info["major"]:
        result = result.filter(
            and_(
                or_(
                    and_(Must.include.contains(i), Must.mname.contains(Major.mname)),
                    Major.mname.contains(i),
                )
                for i in info["major"].split()
            )
        )

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
            result = result.order_by(func.abs(Rank.rank - rank).asc())
    else:
        result = result.order_by(Univ.sid.asc())

    if info["mymust"]:
        mymust = "".join(map(str, info["mymust"]))
        result = result.order_by(Must.must.desc())
        if info["accordation"]:
            what_i_can = get_what_i_can_choose_most(mymust)
            result = result.order_by(Must.must)
        else:
            what_i_can = get_what_i_can_choose(mymust)
        result = result.filter(Must.must.in_(what_i_can))

    result = result.filter(Must.year == info["standard"])
    result = result.group_by(Major.mid)

    if info["utags"]:
        condition = or_(Univ.utags.like("%," + str(i) + ",%") for i in info["utags"])
        result = result.filter(condition)

    if info["nutags"]:
        ncondition = not_(
            and_(Univ.utags.like("%," + str(i) + ",%") for i in info["nutags"])
        )
        result = result.filter(ncondition)

    if info["province"]:
        result = result.filter(Univ.province.in_(info["province"]))

    count = result.count()

    if info["page"]:
        result = result.offset((info["page"] - 1) * 50).limit(50).all()
    else:
        result = result.all()

    result = [
        i if i[3] else (i[0], i[1], i[2], findNearestMust(i[0].mname, info["standard"]))
        for i in result
    ]

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
