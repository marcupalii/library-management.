from flask import render_template, request, session, url_for, redirect, abort
from app import app
from app.models import User
import hashlib

@app.errorhandler(401)
def FUN_401(error):
    return render_template("page_401.html"), 401


@app.errorhandler(403)
def FUN_403(error):
    return render_template("page_403.html"), 403


@app.errorhandler(404)
def FUN_404(error):
    return render_template("page_404.html"), 404


@app.errorhandler(405)
def FUN_405(error):
    return render_template("page_405.html"), 405


@app.route("/")
@app.route('/home')
def home():
    return render_template("home.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route("/login", methods=['GET','POST'])
def login():
    user_name_submitted = request.form.get("name")
    pass_submitted = request.form.get("pw")
    _user = User.query.filter_by(username=user_name_submitted).first()
    print(_user)
    if _user:
        if _user.password == hashlib.sha512(pass_submitted.encode()).hexdigest():
            session["current_user"] = _user.username
            session["current_type"] = _user.type

            print(session.get("current_type"),session.get("current_type"))
            return render_template("account.html")

    return render_template("about.html")


@app.route("/logout")
def logout():
    session.pop("current_user", None)
    session.pop("current_type", None)
    return render_template("about.html")


@app.route("/account")
def account():
    return render_template("account.html")


@app.route("/admin")
def admin():
    return render_template("admin.html")
