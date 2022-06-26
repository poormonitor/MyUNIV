from flask import Blueprint, render_template
from func import login_required, get_must_string
from const import provinces
from models import db
from models.Major import Major
from models.Univ import Univ
from models.Tag import Tag
from models.Rank import Rank
from models.Must import Must
import json

univ_bp = Blueprint("Univ", __name__)


@univ_bp.route("/univ/<int:sid>", methods=["GET"])
@login_required
def univ(sid: int):
    univ = Univ.query.filter_by(sid=sid).first()
    tags = []
    for i in univ.utags.split(","):
        if i:
            tags.append(Tag.query.filter_by(tid=int(i)).first().tname)
    rks = (
        db.session.query(Major, Rank)
        .filter(Major.mid == Rank.mid)
        .filter(Major.sid == univ.sid)
        .order_by(Rank.year.asc())
        .order_by(Rank.rank.asc())
        .all()
    )
    ranks = {}
    for i in rks:
        if i[1].year not in ranks:
            ranks[i[1].year] = []
        ranks[i[1].year].append(i)
    mts = db.session.query(Must).filter(Must.sid == univ.sid).all()
    musts = {}
    for i in mts:
        if i.year not in musts:
            musts[i.year] = []
        content = {
            "must": get_must_string(i.must),
            "mname": i.mname,
            "include": i.include,
        }
        musts[i.year].append(content)
    totals = (
        db.session.query(Rank.year, db.func.sum(Rank.schedule))
        .filter(Rank.mid.in_(db.session.query(Major.mid).filter(Major.sid == sid)))
        .group_by(Rank.year)
        .order_by(Rank.year.asc())
        .all()
    )
    totals = [[str(i[0]), i[1]] for i in totals]
    totals = json.dumps(totals)
    rank = [[str(i[0]), max(j[1].rank for j in i[1])] for i in ranks.items()]
    rank = json.dumps(rank)
    province = provinces[univ.province]
    return render_template(
        "univ.html.j2",
        univ=univ,
        ranks=ranks,
        musts=musts,
        tags=tags,
        total=totals,
        rank=rank,
        province=province,
    )
