from flask import render_template, request, url_for, redirect, abort, jsonify, Response
from app import app, login_manager, db
from app.models import User, Wishlist, EntryWishlist, Book, NextBook, BookSeries, Notifications, Author
from flask_sqlalchemy import Pagination
from app.forms import LoginForm, Search, Wishlist_form
from flask_login import login_user, login_required, logout_user, current_user
from flask import jsonify

import hashlib
import json


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


@app.route("/")
@app.route('/about')
def about():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    else:
        return render_template("about.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return render_template("about.html")


@app.route("/wishlist_delete_entry/<entry_id>", methods=["GET"])
@login_required
def wishlist_delete_entry(entry_id):
    _user = User.query.filter_by(email=current_user.email).first()
    if _user:
        _entry = EntryWishlist.query.filter_by(id=entry_id).first()
        if _entry:
            rank = _entry.rank
            db.session.delete(_entry)
            db.session.commit()

            _wishlist = _user.wishlist
            _entryes = _wishlist.entry_wishlists

            for _entry in _entryes:

                if _entry.rank >= rank:
                    _entry.rank -= 1
                    db.session.commit()

        else:
            return abort(401)
    return redirect(url_for("wishlist"))


@app.route("/add_book_to_wishlist", methods=["POST"])
@login_required
def add_book_to_wishlist():
    _name = request.form.get("name")
    _period = request.form.get("period")
    _rank = int(request.form.get("rank"))
    _book = Book.query.filter_by(name=_name).first()
    if _book:

        _user = User.query.filter_by(email=current_user.email).first()
        _wishlist = _user.wishlist

        _entrywishlist = _wishlist.entry_wishlists
        for _entry in _entrywishlist:

            if _entry.rank >= _rank:
                _entry.rank += 1
                db.session.commit()

        _new_entry = EntryWishlist(wishlist=_wishlist, id_book=_book.id, rank=_rank, period=_period)

        db.session.add(_new_entry)
        db.session.commit()


    else:
        return abort(401)

    return redirect(url_for("wishlist"))


@app.route("/notifications")
@login_required
def notifications():
    _email = current_user.email
    response = []
    if _email:
        _user = User.query.filter_by(email=_email).first()

        _notifications = Notifications.query.filter_by(id_user=_user.id).order_by(Notifications.created_at.desc()).all()

        if _notifications:
            for notification in _notifications:
                response.append([
                    notification.id,
                    notification.content,
                    notification.status,
                    notification.created_at
                ])

        return render_template("notifications.html", notifications=response, id_user=current_user.id)


@app.route("/wishlist")
@login_required
def wishlist():
    _email = current_user.email
    response = []
    if _email:
        _user = User.query.filter_by(email=_email).first()

        _entry_wishlist = EntryWishlist.query.filter_by(id_wishlist=_user.wishlist.id).order_by(
            EntryWishlist.rank.asc()).all()

        if _entry_wishlist:
            for entry in _entry_wishlist:
                _book = Book.query.filter_by(id=entry.id_book).first()
                response.append([
                    entry.rank,
                    _book.name,
                    _book.type,
                    entry.period,
                    entry.created_at,
                    entry.id
                ])

        return render_template("wishlist.html", wishlist=response, id_user=current_user.id)


@app.route("/books_log")
@login_required
def books_log():
    return render_template("books_log.html")


@app.route("/mark_notification_read/", methods=['POST'])
@login_required
def mark_notification_read():
    _email = current_user.email

    if _email:
        print("==", request.data.decode().split("=")[1], "==")
        _user = User.query.filter_by(email=_email).first()
        _notification = Notifications.query.filter_by(
            id_user=_user.id,
            id=int(request.data.decode().split("=")[1])
        ).first()
        if _notification:
            _notification.status = "read"
            db.session.commit()

        return render_template("layout.html", id_user=current_user.id)


@app.route("/get_notification/", methods=['GET'])
@login_required
def get_notification():
    _email = current_user.email
    response = {}
    if _email:
        _user = User.query.filter_by(email=_email).first()
        _notifications = Notifications.query.filter_by(
            id_user=_user.id,
            status="unread"
        )
        if _notifications:
            for _notification in _notifications:
                response.update({
                    str(_notification.id): {
                        'href_': '/notifications',
                        'text_': _notification.content,
                        'date_': _notification.created_at

                    }
                })
        return jsonify({key: response[key] for key in response.keys()})


@app.route("/account")
@login_required
def account():
    _email = current_user.email

    if _email:
        _user = User.query.filter_by(email=_email).first()

        # form = SearchForm()
        # return render_template('account.html', form=form)
        form = Search(search_by_name=False, search_by_type=False, search_by_author=False)
        wishlist_form = Wishlist_form()
        return render_template('account.html', form=form,wishlist_form = wishlist_form)
    else:
        return redirect(url_for('about'))


@app.route("/login")
def login():
    if current_user.is_authenticated:
        if current_user.type == "admin":
            return redirect(url_for('admin'))
        else:
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
            if user.type == "admin":
                return jsonify(data='succes-as-admin')
            else:
                return jsonify(data='succes-as-user')
        else:
            return jsonify(data="invalid-credentials")

    return jsonify(data=form.errors)


@app.route("/admin")
@login_required
def admin():
    return render_template("admin.html")


@app.route("/search_book/", methods=['POST'])
@login_required
def search_book():
    response = {}
    num_list = []

    if current_user.email:
        form = Search()
        if form.validate_on_submit():
            author = ""
            name = ""
            type = ""
            if form.search_substring.data == False:
                author = form.search_author.data if form.search_author.data else '%%'
                name = form.search_name.data if form.search_name.data else '%%'
                type = form.search_type.data if form.search_type.data else '%%'
            else:
                author = '%' + form.search_author.data + '%' if  form.search_author.data else '%%'
                name = '%' + form.search_name.data + '%' if form.search_name.data else '%%'
                type = '%' + form.search_type.data + '%' if form.search_type.data else '%%'

            book_author_join = Book.query \
                .filter(Book.name.like(name) & (Book.type.like(type))) \
                .join(Author, Book.author_id == Author.id) \
                .filter(Author.name.like(author)) \
                .order_by(Book.name) \
                .add_columns(Author.id, Author.name) \
                .paginate(
                    per_page=3,
                    page=form.page_number.data,
                    error_out=True
                )
            if book_author_join:
                for entry in book_author_join.items:
                    response.update({
                        str(entry[0].id): {
                            'author_name': entry[2],
                            'book_name': entry[0].name,
                            'book_type': entry[0].type,
                            'count_book': entry[0].count_free_books
                        }
                    })
                for i in book_author_join.iter_pages(left_edge=2, right_edge=2, left_current=2, right_current=2):
                    num_list.append(i)

            return jsonify(
                data={key: response[key] for key in response.keys()},
                pages_lst=[value for value in num_list]
            )
        return jsonify(data=form.errors)
