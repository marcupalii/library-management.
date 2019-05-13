from flask import render_template, request, url_for, redirect, abort, jsonify, Response
from app import app, login_manager, db
from app.models import User, Wishlist, EntryWishlist, Book, NextBook, BookSeries, Notifications, Author, Log, EntryLog
# from app.forms import LoginForm, Search, Wishlist_form, Reserved_book_date
# from flask_login import login_user, login_required, logout_user, current_user
# from flask import jsonify
# import datetime
# import pytz
# import hashlib
# import json


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


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

