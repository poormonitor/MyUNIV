from flask import Blueprint, redirect, render_template, session, request, url_for
from func import csrf_valid_if_post, admin_required
from tempfile import NamedTemporaryFile
import os
import sys
import subprocess

add_data_bp = Blueprint("AddData", __name__)


@add_data_bp.route("/adddata", methods=["GET", "POST"])
@admin_required
@csrf_valid_if_post
def adddata():
    if request.method == "GET":
        session["csrf"] = os.urandom(16).hex()
        return render_template("adddata.html.j2", csrf=session["csrf"])

    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

    if "year" in request.form:
        year = int(request.form["year"])
        xlsx = request.files["xlsx"]
        filename = NamedTemporaryFile(delete=False, suffix=".xlsx").name
        xlsx.save(filename)
        subprocess.Popen(
            [sys.executable, os.path.join(path, "import.py"), filename, str(year)]
        )
    elif "conn" in request.form:
        subprocess.Popen([sys.executable, os.path.join(path, "conn.py")])
    elif "clean" in request.form:
        from func import cleanAll

        cleanAll()

    session["notice"] = "数据导入成功"
    return redirect(url_for("Index.index"))
