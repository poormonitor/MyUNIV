from datetime import datetime, timedelta
from typing import Tuple

from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from config import get_secret_key
from models import get_db
from models.user import User

SECRET_KEY = get_secret_key()
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/user/token")
credentials_exception = HTTPException(
    status_code=401,
    detail="无法验证用户信息。",
    headers={"WWW-Authenticate": "Bearer"},
)


def create_access_token(
    uid: str, expires_delta: timedelta = timedelta(hours=1), **extra_data
) -> str:
    to_encode = extra_data.copy()
    expire = datetime.utcnow() + expires_delta

    to_encode.update({"uid": uid})
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        uid = payload.get("uid")

        if not uid:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    return uid


async def admin_required(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        admin = payload.get("admin", False)

    except JWTError:
        raise credentials_exception

    if not admin:
        raise HTTPException(status_code=401, detail="需要管理员权限。")

    return True


async def is_admin(request: Request) -> bool:
    try:
        token: str = await oauth2_scheme(request)
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        admin = payload.get("admin", False)
    except:
        return False

    return admin


async def get_user_token(identity: Tuple[bool, str] = Depends(get_current_user)) -> str:
    token = identity[1]

    return token


async def get_user_identity(
    request: Request, db: Session = Depends(get_db)
) -> Tuple[bool, str]:
    idn = False
    try:
        token: str = await oauth2_scheme(request)
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        uid: str = payload.get("uid")
        assert uid is not None
        idn = True
    except:
        uid: str = request.headers.get("X-MyExam-Token", "")
        user_cnt = db.query(User).filter_by(uid=uid).count()
        if user_cnt:
            raise HTTPException(status_code=401, detail="签名无效。")

    return idn, uid


def hash_passwd(passwd: str) -> str:
    return pwd_context.hash(passwd)


def verify_passwd(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)
