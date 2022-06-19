from flask import Blueprint, redirect, render_template, session, request, url_for
from func import valid_csrf, admin_required, process_excel
import os

add_data_bp = Blueprint('AddData', __name__)


@add_data_bp.route('/adddata', methods=['GET', 'POST'])
@admin_required
def adddata():
    if request.method == "GET":
        session['csrf'] = os.urandom(16).hex()
        return render_template('adddata.html.j2', csrf=session["csrf"])
    if not valid_csrf():
        return redirect(url_for('AddData.adddata'))
    year = int(request.form["year"])
    xlsx = request.files['xlsx']
    process_excel(xlsx, year)
    session["notice"] = "数据导入成功"
    return redirect(url_for('Index.index'))
