from flask import render_template
from app import app
from flask_login import login_required


@app.route("/admin")
@login_required
def admin():
    return render_template("admin.html")
