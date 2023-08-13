from flask import Blueprint, render_template
from func import login_required, get_must_string
from models.Major import Major
from models.Univ import Univ
from models.Tag import Tag
from models.Rank import Rank
from models.Conne import Conne
from models.Must import Must
from models import db
import json

major_bp = Blueprint("Major", __name__)


@major_bp.route("/major/<int:mid>", methods=["GET"])
@login_required
def major(mid: int):
    major = Major.query.filter_by(mid=mid).first()
    univ = Univ.query.filter_by(sid=major.sid).first()
    ranks = Rank.query.filter_by(mid=mid).order_by(Rank.year.asc()).all()
    must = (
        db.session.query(Must, Major, Conne)
        .filter(Major.sid == major.sid)
        .filter(Major.mid == major.mid)
        .filter(Must.sid == major.sid)
        .filter(Conne.year == Must.year)
        .filter(Conne.mmid == Must.mmid)
        .filter(Conne.mid == Major.mid)
        .order_by(Must.year.asc())
    )
    musts = []
    include = []
    for i in must:
        content = {
            "year": i[0].year,
            "must": get_must_string(i[0].must),
            "mname": i[0].mname,
            "include": i[0].include,
        }
        include += list(i[0].include.split("、"))
        musts.append(content)
    include = list(set(include))
    tags = Tag.query.filter_by().all()
    totals = [[str(i.year), i.schedule] for i in ranks]
    totals = json.dumps(totals)
    rank = [[str(i.year), i.rank] for i in ranks]
    rank = json.dumps(rank)
    return render_template(
        "major.html.j2",
        major=major,
        ranks=ranks,
        tags=tags,
        univ=univ,
        must=musts,
        total=totals,
        rank=rank,
        include=include,
    )
