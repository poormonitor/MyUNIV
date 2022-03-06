from flask import Blueprint, render_template, request
from func import login_required
from models import db
from models.Major import Major
from models.Univ import Univ
from models.Tag import Tag
from models.Rank import Rank
from models.Must import Must

univ_bp = Blueprint('Univ', __name__)


@univ_bp.route('/univ/<int:sid>', methods=['GET'])
@login_required
def univ(sid: int):
    univ = Univ.query.filter_by(sid=sid).first()
    tags = []
    for i in univ.utags.split(","):
        if i:
            tags.append(Tag.query.filter_by(tid=int(i)).first().tname)
    rks = db.session.query(Major, Rank).filter(Major.mid == Rank.mid).filter(
        Major.sid == univ.sid).all()
    ranks = {}
    for i in rks:
        if i[1].year not in ranks:
            ranks[i[1].year] = []
        ranks[i[1].year].append(i)
    mts = db.session.query(Major, Must).filter(Major.mid == Must.mid).filter(
        Major.sid == univ.sid).all()
    musts = {}
    for i in mts:
        if i[1].year not in musts:
            musts[i[1].year] = []
        musts[i[1].year].append(i)
    return render_template('univ.html',
                           univ=univ,
                           ranks=ranks,
                           musts=musts,
                           tags=tags)
