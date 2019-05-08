
from flask import render_template, url_for, redirect
from app import app
from flask_login import current_user
@app.route("/")
@app.route('/about')
def about():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    else:
        return render_template("about.html")
