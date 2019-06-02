
from flask import render_template, url_for, redirect, jsonify, request, json
from app import app, db
from flask_login import current_user, login_required
from app.forms import Wishlist_settings, Change_password, Profile
import hashlib
from app.models import User
import os
from app import APP_ROOT

@app.route("/users")
@login_required
def users():
    return render_template("users.html")

@app.route('/add_user/',methods=["POST"])
@login_required
def add_user():
    target = os.path.join(APP_ROOT, 'images/')
    print(target)

    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist("file"):
        print(file)
        filename = file.filename
        destination = "/".join([target, filename])
        print(destination)
        file.save(destination)
    return redirect(url_for('users'))