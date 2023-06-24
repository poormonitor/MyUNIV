import os
import subprocess
import sys
from tempfile import NamedTemporaryFile
from pydantic import BaseModel

from fastapi import APIRouter, UploadFile, Form, Depends
from sqlalchemy.orm import Session
from misc.func import get_school_name, unifyBracket, cleanAll
from models import get_db
from models.tag import Tag
from models.univ import Univ

router = APIRouter()


@router.post("/data")
def add_data(file: UploadFile, year: int = Form(...)):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

    filename = NamedTemporaryFile(delete=False, suffix=".xlsx").name
    with open(filename, "wb") as fp:
        fp.write(file.file.read())

    subprocess.Popen(
        [sys.executable, os.path.join(path, "import.py"), filename, str(year)]
    )

    return {"result": "success"}


class SetTag(BaseModel):
    tag: str
    school: str


@router.post("/tag")
def set_tag(data: SetTag, db: Session = Depends(get_db)):
    if (a := db.query(Tag).filter_by(tname=data.tag).first()) is None:
        a = Tag(tname=data.tag)
        db.add(a)
        db.flush()
    tag_id = a.tid

    for i in data.school.splitlines():
        i, _ = get_school_name(i)
        i = unifyBracket(i)

        if (a := db.query(Univ).filter_by(uname=i).first()) is None:
            a = Univ(uname=i)
            db.add(a)
            db.flush()

        utags = [i for i in a.utags.split(",") if i != ""]
        if tag_id not in utags:
            utags.append(str(tag_id))
            utags = list(set(utags))
            a.utags = "," + ",".join(utags) + ","

    db.commit()

    return {"result": "success"}


@router.post("/conn")
def go_conn():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
    subprocess.Popen([sys.executable, os.path.join(path, "conn.py")])

    return {"result": "success"}


@router.post("/clean")
def go_clean():
    cleanAll()

    return {"result": "success"}
