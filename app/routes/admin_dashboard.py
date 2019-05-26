from flask import render_template
from app import app
from flask_login import login_required


@app.route("/admin_dashboard/")
@login_required
def admin_dashboard():
    return render_template("admin.html")

@app.route("/users")
@login_required
def users():
    return render_template("users.html")
