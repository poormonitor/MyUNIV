from typing import List, Tuple

from pydantic import BaseModel


class OneTag(BaseModel):
    tid: str
    tname: str


class OneUniv(BaseModel):
    sid: str
    uname: str
    utags: List[int]
    province: int


class OneRank(BaseModel):
    rmid: int
    year: int
    rank: int
    score: int
    schedule: int
    mid: int


class OneMajor(BaseModel):
    mid: int
    mname: str
    sid: int


class OneMust(BaseModel):
    mmid: int
    mname: str
    year: int
    sid: int
    must: int
    include: str


def trans_utags(univ):
    data = vars(univ)
    if not isinstance(data["utags"], list):
        if data["utags"] == ",,":
            data["utags"] = []
        else:
            data["utags"] = list(map(int, data["utags"].strip(",").split(",")))
    return data


def parse_result(rs):
    return [
        (
            OneMajor.parse_obj(vars(i[0])),
            OneUniv.parse_obj(trans_utags(i[1])),
            OneRank.parse_obj(vars(i[2])),
            OneMust.parse_obj(vars(i[3])),
        )
        for i in rs
    ]


class QueryResult(BaseModel):
    total: int
    result: List[Tuple[OneMajor, OneUniv, OneRank, OneMust]]
