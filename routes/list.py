from typing import List, Tuple

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from misc.func import lru_cache_ignored
from misc.model import OneTag
from models import get_db
from models.must import Must
from models.rank import Rank
from models.tag import Tag

router = APIRouter()


@router.get("/ranks")
def get_available_rank(db: Session = Depends(get_db)) -> List[int]:
    years = db.query(Rank.year).group_by(Rank.year).order_by(Rank.year.asc()).all()
    years = [i[0] for i in years]
    return years


@router.get("/musts")
def get_available_must(db: Session = Depends(get_db)) -> List[int]:
    years = db.query(Must.year).group_by(Must.year).order_by(Must.year.asc()).all()
    years = [i[0] for i in years]
    return years


@lru_cache_ignored(None)
def get_sums_helper(db: Session) -> int:
    totals = db.query(Rank.year, func.sum(Rank.schedule))
    totals = totals.group_by(Rank.year)
    totals = totals.order_by(Rank.year.asc())
    totals = totals.all()

    years = [(i[0], i[1]) for i in totals]
    return years


@router.get("/sums")
def get_sums(db: Session = Depends(get_db)) -> List[Tuple[int, int]]:
    years = get_sums_helper(db)
    return years


@router.get("/tags")
def get_available_tags(db: Session = Depends(get_db)) -> List[OneTag]:
    tags = db.query(Tag).all()
    tags = [OneTag(**vars(i)) for i in tags]
    return tags
