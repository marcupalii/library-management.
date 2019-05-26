from flask import render_template, url_for, redirect, jsonify
from app import app, db
from flask_login import current_user, login_required
from app.forms import New_Book, Choose_Author
import hashlib
from app.models import User


@app.route('/books')
@login_required
def books():
    if current_user.type != "admin":
        return render_template("page_403.html")
    new_book = New_Book()
    choose_author = Choose_Author()
    return render_template(
        "books.html",
        new_book=new_book,
        choose_author=choose_author
    )


@app.route('/add_new_book/',methods=["POST"])
@login_required
def add_new_book():
    if current_user.type != "admin":
        return render_template("page_403.html")
    new_book = New_Book()

    if new_book.validate_on_submit():
        print(
            new_book.name.data,
            new_book.type.data,
            new_book.series.data,
            new_book.author.data
        )
        return jsonify(data={
            'id': 3,
            'code': 200
        })
    else:
        print(new_book.errors)
        return jsonify(data=new_book.errors)