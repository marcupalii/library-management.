from flask import render_template, request, url_for, redirect, abort, jsonify, Response
from app import app, login_manager, db
from app.models import User, Wishlist, EntryWishlist, Book, NextBook, BookSeries, Notifications, Author

from app.forms import LoginForm, SearchForm, WishlistForm
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


@app.route("/books_reservation")
@login_required
def books_reservation():
    return render_template("books_reservation.html")


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

        form = SearchForm()
        return render_template('account.html', form=form)
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


@app.route('/autocomplete/<option>/', methods=['GET'])
@login_required
def autocomplete(option):
    if current_user.email:

        print(option, type(option))
        if option == "1":
            books_name = Book.query.with_entities(Book.name).all()
            return Response(json.dumps([el[0] for el in books_name]), mimetype='application/json')
        elif option == "2":
            books_type = Book.query.with_entities(Book.type).all()
            return Response(json.dumps([el[0] for el in books_type]), mimetype='application/json')
        elif option == "3":
            books_author = Author.query.with_entities(Author.name).all()
            return Response(json.dumps([el[0] for el in books_author]), mimetype='application/json')


@app.route("/process_search_form/", methods=['POST'])
@login_required
def process_search_form():
    response = {}
    num_list = []

    if current_user.email:

        form = SearchForm()
        if form.validate_on_submit():

            print(form.autocomp.data, form.option.data)

            if form.option.data == "1":
                books = Book.query.filter_by(name=form.autocomp.data).order_by(Book.name).paginate(
                    per_page=3,
                    page=form.page_number.data,
                    error_out=True
                )

                for book in books.items:
                    author = Author.query.filter_by(id=book.author_id).first()
                    response.update({
                        str(book.id): {
                            'author_name': author.name,
                            'book_name': book.name,
                            'book_type': book.type,
                            'count_book': book.count_free_books
                        }
                    })

                for i in books.iter_pages(left_edge=2, right_edge=2, left_current=2, right_current=2):
                    num_list.append(i)

            elif form.option.data == "2":
                books = Book.query.filter_by(type=form.autocomp.data).order_by(Book.name).paginate(
                    per_page=3,
                    page=form.page_number.data,
                    error_out=True
                )

                for book in books.items:
                    author = Author.query.filter_by(id=book.author_id).first()
                    response.update({
                        str(book.id): {
                            'author_name': author.name,
                            'book_name': book.name,
                            'book_type': book.type,
                            'count_book': book.count_free_books
                        }
                    })
                for i in books.iter_pages(left_edge=2, right_edge=2, left_current=2, right_current=2):
                    num_list.append(i)

            elif form.option.data == "3":
                author = Author.query.filter_by(name=form.autocomp.data).first()
                if author:
                    books = Book.query.filter_by(author_id=author.id).order_by(Book.name).paginate(
                        per_page=3,
                        page=form.page_number.data,
                        error_out=True
                    )

                    for book in books.items:
                        response.update({
                            str(book.id): {
                                'author_name': author.name,
                                'book_name': book.name,
                                'book_type': book.type,
                                'count_book': book.count_free_books
                            }
                        })
                    for i in books.iter_pages(left_edge=2, right_edge=2, left_current=2, right_current=2):
                        num_list.append(i)

            return jsonify(
                data={key: response[key] for key in response.keys()},
                pages_lst=[value for value in num_list]
            )

        return jsonify(data=form.errors)
