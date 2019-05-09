from flask import render_template, url_for, redirect
from app import app
from flask_login import current_user, login_required


@app.route('/profile')
@login_required
def profile():
    return render_template("profile.html")
