from flask import Blueprint, render_template, session
from func import login_required, get_must_string
from models.Major import Major
from models.Univ import Univ
from models.Tag import Tag
from models.Rank import Rank
from models.Must import Must
from models import db
import json

my_major_bp = Blueprint('MyMajor', __name__)


@my_major_bp.route('/my', methods=['GET'])
@login_required
def mymajor():
    mymajor = session["my"]
    result = db.session.query(Major, Univ, Rank, Must)
    result = result.outerjoin(Major, Major.mid == Rank.mid)
    result = result.filter(Major.mid.in_(mymajor))
    result = result.outerjoin(Univ, Univ.sid == Major.sid)
    result = result.outerjoin(
        Must, db.and_(Must.sid == Major.sid,
                      Major.mname.contains(Must.mname))).group_by(Major.mid)
    result = result.order_by(Rank.score.desc())
    result = result.all()
    musts = [(get_must_string(i[3].must), i[3].year) if i[3] else ""
             for i in result]
    return render_template('mymajor.html',
                           result=enumerate(result),
                           cnt=len(result),
                           musts=musts)
