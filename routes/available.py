from typing import Dict, List

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from models import get_db
from models.rank import Rank
from models.tag import Tag

router = APIRouter()


@router.get("/ranks")
def get_available_rank(db: Session = Depends(get_db)) -> List[int]:
    years = db.query(Rank.year).group_by(Rank.year).order_by(Rank.year.asc()).all()
    return years


@router.get("/sums")
def get_sums(db: Session = Depends(get_db)) -> Dict[int, int]:
    totals = (
        db.query(Rank.year, func.sum(Rank.schedule))
        .group_by(Rank.year)
        .order_by(Rank.year.asc())
        .all()
    )
    years = {i[0]: i[1] for i in totals}
    return years


class OneTag(BaseModel):
    tid: str
    tname: str


@router.get("/tags")
def get_available_tags(db: Session = Depends(get_db)) -> List[OneTag]:
    tags = db.query(Tag).all()
    return tags
