from flask import Blueprint, render_template
from func import login_required
from models.Major import Major
from models.Univ import Univ
from models.Tag import Tag
from models.Rank import Rank
from models.Must import Must

major_bp = Blueprint('Major', __name__)


@major_bp.route('/major/<int:mid>', methods=['GET'])
@login_required
def major(mid: int):
    major = Major.query.filter_by(mid=mid).first()
    univ = Univ.query.filter_by(sid=major.sid).first()
    ranks = Rank.query.filter_by(mid=mid).order_by(Rank.year.desc()).all()
    must = Must.query.filter_by(mid=mid).order_by(Must.year.desc()).all()
    tags = Tag.query.filter_by().all()
    return render_template('major.html',
                           major=major,
                           ranks=ranks,
                           tags=tags,
                           univ=univ,
                           must=must)
