from datetime import timedelta
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.orm import Session

from misc.auth import create_access_token, get_current_user, hash_passwd, verify_passwd
from models import get_db
from models.user import User

router = APIRouter()


class LoginForm(BaseModel):
    uid: str
    passwd: str


class UserToken(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.post("/login")
def login(form: LoginForm, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(uid=form.uid).first()

    if not user:
        raise HTTPException(status_code=400, detail="用户不存在")

    if not verify_passwd(form.passwd, user.passwd):
        raise HTTPException(status_code=400, detail="密码错误")

    token = create_access_token(
        user.uid, timedelta(hours=2), admin=user.admin, name=user.name
    )
    user.last_login = func.now()
    db.commit()

    return UserToken(access_token=token)


class UserPasswd(BaseModel):
    old: str
    new: str


@router.post("/passwd")
def passwd(
    data: UserPasswd,
    db: Session = Depends(get_db),
    uid: str = Depends(get_current_user),
):
    user = db.query(User).filter_by(uid=uid).first()

    if not verify_passwd(data.old, user.passwd):
        raise HTTPException(status_code=400, detail="原密码错误")

    user.passwd = hash_passwd(data.new)
    db.commit()

    return {"result": "success"}
