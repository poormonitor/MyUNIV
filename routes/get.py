import hashlib
from itertools import groupby
from typing import Dict, List, Tuple

import pandas as pd
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy import and_, func, not_, or_
from sqlalchemy.orm import Session
import tempfile

from misc.auth import get_current_user
from misc.func import findNearestMust, get_must_string
from misc.model import (
    OneMajor,
    OneMust,
    OneRank,
    OneUniv,
    QueryResult,
    parse_result,
    trans_utags,
)
from models import get_db
from models.conne import Conne
from models.major import Major
from models.must import Must
from models.rank import Rank
from models.univ import Univ
from models.user import User

router = APIRouter()


class UnivResult(BaseModel):
    uname: str
    utags: List[int]
    province: int
    musts: List[OneMust]
    ranks: List[Tuple[OneRank, OneMajor]]


@router.get("/univ")
def get_univ(sid: int, db: Session = Depends(get_db)) -> UnivResult:
    univ = db.query(Univ).filter_by(sid=sid).first()
    if not univ:
        raise HTTPException(status_code=404, detail="学校不存在")

    musts = db.query(Must).filter_by(sid=sid).all()
    musts = [OneMust.parse_obj(vars(i)) for i in musts]

    ranks = db.query(Rank, Major).join(Major, Major.mid == Rank.mid, isouter=True)
    ranks = ranks.filter(Major.sid == sid).all()
    ranks = [
        (OneRank.parse_obj(vars(i[0])), OneMajor.parse_obj(vars(i[1]))) for i in ranks
    ]

    data = trans_utags(univ) | {"musts": musts, "ranks": ranks}

    return UnivResult.parse_obj(data)


class MajorResult(BaseModel):
    mid: int
    mname: str
    univ: OneUniv
    musts: List[OneMust]
    ranks: List[OneRank]


@router.get("/major")
def get_major(mid: int, db: Session = Depends(get_db)) -> MajorResult:
    major = db.query(Major).filter_by(mid=mid).first()
    if not major:
        raise HTTPException(status_code=404, detail="专业不存在")

    univ = db.query(Univ).filter_by(sid=major.sid).first()
    univ = trans_utags(univ)

    musts = db.query(Must).join(Conne, Conne.mmid == Must.mmid)
    musts = musts.filter(Conne.mid == major.mid).all()
    musts = [OneMust.parse_obj(vars(i)) for i in musts]

    ranks = db.query(Rank).filter_by(mid=major.mid).all()
    ranks = [OneRank.parse_obj(vars(i)) for i in ranks]

    data = vars(major) | {"univ": univ, "musts": musts, "ranks": ranks}

    return MajorResult.parse_obj(data)


@router.get("/score")
def get_score(year: int, score: int, db: Session = Depends(get_db)):
    rank = (
        db.query(Rank)
        .filter_by(year=year)
        .filter(Rank.rank != 0)
        .order_by(func.abs(Rank.score - score).asc())
        .order_by(Rank.rank.desc())
        .first()
    )

    if not rank:
        rank = 0
    elif rank.score != score:
        s_rank = (
            db.query(Rank)
            .filter_by(year=year)
            .filter(Rank.rank != 0)
            .order_by(Rank.rank.asc(), func.abs(Rank.score - score).desc())
            .first()
        )
        rank = (rank.rank + s_rank.rank) // 2 if s_rank else rank.rank
    else:
        rank = rank.rank

    return {"rank": rank}


class MyQuery(BaseModel):
    year: int
    standard: int


@router.post("/my")
def get_my_major(
    form: MyQuery, db: Session = Depends(get_db), uid=Depends(get_current_user)
) -> QueryResult:
    user = db.query(User.mymajor).filter_by(uid=uid).first()
    majors = list(map(int, user.mymajor.split(","))) if user.mymajor else []

    result = db.query(Major, Univ, Rank, Must)
    result = result.select_from(Rank)
    result = result.outerjoin(Major, Major.mid == Rank.mid)
    result = result.outerjoin(Univ, Univ.sid == Major.sid)
    result = result.outerjoin(Conne, Conne.mid == Rank.mid)
    result = result.outerjoin(
        Must, and_(Conne.mmid == Must.mmid, Conne.year == Must.year)
    )
    result = result.filter(Major.mid.in_(majors))
    result = result.filter(Rank.year == form.year)
    result = result.filter(Must.year == form.standard)
    result = result.order_by(Rank.rank.asc())

    count = result.count()
    result = result.all()

    return QueryResult(total=count, result=parse_result(result))


class MajorsQuery(BaseModel):
    majors: List[int]
    year: int
    standard: int


@router.post("/majors")
def get_majors(form: MajorsQuery, db: Session = Depends(get_db)) -> QueryResult:
    if len(form.majors) > 200:
        raise HTTPException(status_code="403", detail="项目过多")

    result = db.query(Major, Univ, Rank, Must)
    result = result.select_from(Rank)
    result = result.outerjoin(Major, Major.mid == Rank.mid)
    result = result.outerjoin(Univ, Univ.sid == Major.sid)
    result = result.outerjoin(Conne, Conne.mid == Rank.mid)
    result = result.outerjoin(
        Must, and_(Conne.mmid == Must.mmid, Conne.year == Must.year)
    )
    result = result.filter(Major.mid.in_(form.majors))
    result = result.filter(Rank.year == form.year)
    result = result.filter(Must.year == form.standard)
    result = result.order_by(Rank.rank.asc())

    count = result.count()
    result = result.all()

    return QueryResult(total=count, result=parse_result(result))


@router.post("/excel")
def get_my_excel(
    form: MajorsQuery, db: Session = Depends(get_db), uid=Depends(get_current_user)
) -> QueryResult:
    user = db.query(User.mymajor).filter_by(uid=uid).first()
    majors = list(map(int, user.mymajor.split(","))) if user.mymajor else []

    result = db.query(Major, Univ, Rank, Must)
    result = result.select_from(Rank)
    result = result.outerjoin(Major, Major.mid == Rank.mid)
    result = result.outerjoin(Univ, Univ.sid == Major.sid)
    result = result.outerjoin(Conne, Conne.mid == Rank.mid)
    result = result.outerjoin(
        Must, and_(Conne.mmid == Must.mmid, Conne.year == Must.year)
    )
    result = result.filter(Major.mid.in_(majors))
    result = result.filter(Rank.year == form.year)
    result = result.filter(Must.year == form.standard)
    result = result.order_by(Rank.rank.asc())

    result = result.all()

    result = [
        i if i[3] else (i[0], i[1], i[2], findNearestMust(i[0], form.year))
        for i in result
    ]

    data = [
        (
            item[1].uname,
            item[0].mname,
            item[2].schedule,
            item[2].year,
            item[2].rank,
            item[2].score,
            get_must_string(item[3].must) if item[3] else "",
            item[3].year if item[3] else "",
        )
        for item in result
    ]

    df = pd.DataFrame(
        data, columns=["学校名称", "专业名称", "招生计划", "年份", "位次号", "录取分数", "选考科目", "选考科目标准"]
    )

    with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as tmp_file:
        file_path = tmp_file.name
        df.to_excel(file_path, index=False, sheet_name="志愿信息")

    return FileResponse(file_path, filename="MyUNIV_Export.xlsx")
