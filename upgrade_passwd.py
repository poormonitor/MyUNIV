from models.user import User
from misc.auth import hash_passwd
from models import get_db

db = list(get_db())[0]
for i in db.query(User).all():
    if i.passwd[0] != "$":
        i.passwd = hash_passwd(i.passwd)
db.commit()