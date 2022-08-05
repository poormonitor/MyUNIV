from flask import Blueprint, render_template, session, request
from func import login_required, get_must_string, findNearestMust
from models.Major import Major
from models.Univ import Univ
from models.Rank import Rank
from models.Conne import Conne
from models.Must import Must
from models import db

my_major_bp = Blueprint("MyMajor", __name__)


@my_major_bp.route("/my", methods=["GET"])
@login_required
def mymajor():
    mymajor = session["my"]

    last_year = (
        a.year
        if (
            a := db.session.query(Rank.year)
            .distinct()
            .order_by(Rank.year.desc())
            .first()
        )
        else 0
    )
    must_last_year = (
        a.year
        if (
            a := db.session.query(Must.year)
            .distinct()
            .order_by(Must.year.desc())
            .first()
        )
        else 0
    )

    year = last_year if "year" not in request.args else int(request.args.get("year"))
    standard = (
        must_last_year
        if "standard" not in request.args
        else int(request.args.get("standard"))
    )

    result = db.session.query(Major, Univ, Rank, Must)
    result = result.outerjoin(Major, Major.mid == Rank.mid)
    result = result.filter(Major.mid.in_(mymajor))
    result = result.filter(Rank.year == year)
    result = result.filter(Must.year == standard)
    result = result.outerjoin(Univ, Univ.sid == Major.sid)
    result = result.outerjoin(Conne, db.and_(Conne.mid == Major.mid))
    result = result.outerjoin(
        Must, db.and_(Conne.mmid == Must.mmid, Conne.year == Must.year)
    )
    result = result.group_by(Major.mid)
    result = result.order_by(Rank.score.desc())
    result = result.all()

    result = [
        i if i[3] else (i[0], i[1], i[2], findNearestMust(i[0], year)) for i in result
    ]
    musts = [(get_must_string(i[3].must), i[3].year) if i[3] else "" for i in result]
    must_year_available = [
        i.year for i in Must.query.group_by(Must.year).order_by(Must.year.desc()).all()
    ]
    rank_year_available = [
        i.year for i in Rank.query.group_by(Rank.year).order_by(Rank.year.desc()).all()
    ]
    return render_template(
        "mymajor.html.j2",
        result=enumerate(result),
        cnt=len(result),
        musts=musts,
        must_standard=must_year_available,
        rank_years=rank_year_available,
        year=year,
        standard=standard,
    )
