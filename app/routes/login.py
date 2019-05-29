
from flask import render_template, url_for, redirect, jsonify
from app import app
from app.models import User
from app.forms import LoginForm
from flask_login import login_user, current_user, login_required, logout_user, login_manager
import hashlib


@app.route("/login")
def login():
    if current_user.is_authenticated:
            return redirect(url_for('account'))

    form = LoginForm()
    return render_template('login.html', form=form)


@app.route("/process_login_form", methods=['POST'])
def process_login_form():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(
            email=form.email.data,
            password=hashlib.sha512(form.password.data.encode()).hexdigest()
        ).first()
        if user:
            login_user(user, remember=form.remember.data)
            return jsonify(data={
                'status': 200
            })

        else:
            return jsonify(data="invalid-credentials")

    return jsonify(data=form.errors)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return render_template("about.html")

