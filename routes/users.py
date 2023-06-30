from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.sql import or_

from misc.auth import hash_passwd
from models import get_db
from models.user import User

router = APIRouter()


class Users(BaseModel):
    uid: str
    name: str
    admin: bool
    last_login: datetime


@router.get("/list")
def list_users(s: str = "", page: int = 0, db: Session = Depends(get_db)):
    query = db.query(User).filter(or_(User.name.contains(s), User.uid.contains(s)))
    query = query.order_by(User.last_login.desc())

    cnt = query.count()
    users = query.offset((page - 1) * 10).limit(10).all()

    return {"cnt": cnt, "users": [Users(**vars(i)) for i in users]}


class DelUser(BaseModel):
    uid: str


@router.post("/delete")
def delete_user(data: DelUser, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(uid=data.uid).first()

    if not user:
        raise HTTPException(status_code=404, detail="用户未找到。")

    db.delete(user)
    db.commit()
    return {"result": "success"}


class NewUser(BaseModel):
    uid: str
    name: str
    passwd: str


@router.post("/new")
def new_user(data: NewUser, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(uid=data.uid).first()
    if user:
        raise HTTPException(status_code=404, detail="用户已存在")

    user = User(uid=data.uid, name=data.name, passwd=hash_passwd(data.passwd))
    db.add(user)
    db.commit()

    return {"result": "success"}


class PasswdModify(BaseModel):
    uid: str
    passwd: str


@router.post("/passwd")
def modify_password(data: PasswdModify, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(uid=data.uid).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户未找到。")

    user.passwd = hash_passwd(data.passwd)
    db.commit()
    return {"result": "success"}


class SwitchAdmin(BaseModel):
    uid: str
    admin: bool


@router.post("/admin")
def switch_admin(data: SwitchAdmin, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(uid=data.uid).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户未找到。")

    user.admin = data.admin
    db.commit()
    return {"result": "success"}
