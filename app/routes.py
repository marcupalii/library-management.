from flask import render_template, request, url_for, redirect, abort, jsonify, Response
from app import app, login_manager, db
from app.models import User, Wishlist, EntryWishlist, Book, NextBook, BookSeries, Notifications, Author
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
    user = User.query.filter_by(email=current_user.email).first()
    per_page = 3
    rank = 0
    if user:
        entry = EntryWishlist.query.filter_by(id=entry_id).first()
        if entry:
            rank = entry.rank
            db.session.delete(entry)
            db.session.commit()

            wishlist = user.wishlist
            entryes = wishlist.entry_wishlists

            for entry in entryes:
                if entry.rank >= rank:
                    entry.rank -= 1
                    db.session.commit()

        else:
            return abort(401)

    total = EntryWishlist.query.filter_by(id_wishlist=current_user.wishlist.id).count()
    page = 1
    total_pages = 1

    if rank > per_page:
       page = rank // per_page if rank % per_page == 0 else (rank // per_page) + 1

    if total > total_pages:
        total_pages = total // per_page if total % per_page == 0 else (total // per_page) +1

    if page > total_pages:
        page = total_pages
    return redirect(url_for("wishlist",page=page,book_id=0))


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


@app.route("/wishlist/page/<page>/focus=<book_id>/")
@login_required
def wishlist(page,book_id):

    _email = current_user.email
    response = []
    if _email:
        user = User.query.filter_by(email=_email).first()

        entry_wishlist = EntryWishlist.query \
            .filter_by(id_wishlist=user.wishlist.id) \
            .order_by(EntryWishlist.rank.asc())\
            .paginate(per_page=3,
                page=int(page),
                error_out=True
            )

        if entry_wishlist:
            for entry in entry_wishlist.items:
                _book = Book.query.filter_by(id=entry.id_book).first()
                response.append([
                    entry.rank,
                    _book.name,
                    _book.type,
                    entry.period,
                    entry.created_at,
                    entry.id
                ])


        next_url = url_for('wishlist', page=entry_wishlist.next_num, book_id=book_id) \
            if entry_wishlist.has_next else url_for('wishlist', page=page, book_id=0)
        prev_url = url_for('wishlist', page=entry_wishlist.prev_num,  book_id=book_id) \
            if entry_wishlist.has_prev else url_for('wishlist', page=page, book_id=0)

        return render_template(
            'wishlist.html',
            wishlist=response,
            id_user=current_user.id,
            next_url=next_url,
            prev_url=prev_url
        )

        # return render_template("wishlist.html", wishlist=response, id_user=current_user.id)


@app.route("/wishlist_book/<book_id>/",methods=["GET"])
@login_required
def wishlist_book(book_id):
    book = EntryWishlist.query.filter_by(id_book=book_id).first()
    per_page = 3
    page = 1
    total_pages = 1

    total = EntryWishlist.query.filter_by(id_wishlist=current_user.wishlist.id).count()

    if book.rank > per_page:
        page = book.rank // per_page if book.rank % per_page == 0 else (book.rank // per_page) + 1

    if total > per_page:
        total_pages = total // per_page if total % per_page == 0 else (total // per_page) + 1

    if page > total_pages:
        page = total_pages


    return jsonify({
        "url":"/wishlist/page/{}/focus={}".format(page,book.rank),
        "rank":book.rank
    })



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

        form = Search(search_by_name=False, search_by_type=False, search_by_author=False)
        wishlist_form = Wishlist_form()

        nr = EntryWishlist.query.filter_by(id_wishlist=_user.wishlist.id).count()

        if nr:
            wishlist_form.rank.label = "Rank({}-{})".format(1, nr + 1)
        else:
            wishlist_form.rank.label = "Rank({})".format(1)
        print(wishlist_form.rank.label)
        return render_template('account.html', form=form, wishlist_form=wishlist_form)
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


@app.route("/add_to_wishlist/", methods=['POST'])
@login_required
def add_to_wishlist():
    if current_user.email:
        form = Wishlist_form()
        if form.validate_on_submit():
            print("book_id= {},   nr_of_days= {}, rank={} ".format(form.book_id.data, form.days_number.data,
                                                                   form.rank.data))


            book = Book.query.filter_by(id=form.book_id.data).first()
            if book:
                wishlist = current_user.wishlist

                entrywishlist = wishlist.entry_wishlists
                for entry in entrywishlist:

                    if entry.rank >= form.rank.data:
                        entry.rank += 1
                        db.session.commit()

                new_entry = EntryWishlist(wishlist=wishlist, id_book=book.id, rank=form.rank.data, period=form.days_number.data)

                db.session.add(new_entry)
                db.session.commit()
            nr = EntryWishlist.query.filter_by(id_wishlist=current_user.wishlist.id).count()
            return jsonify(data=nr + 1)
        print(form.errors)
        return jsonify(data=form.errors)


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
                author = '%' + form.search_author.data + '%' if form.search_author.data else '%%'
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
                    entry_wishlist = EntryWishlist.query.filter_by(
                        id_wishlist=current_user.wishlist.id,
                        id_book= entry[0].id
                    ).first()
                    status = ""
                    if entry_wishlist:
                        status = "Already in wishlist"
                    elif entry[0].count_free_books <= 3:
                        status ="Unavailable"
                    else:
                        status = "Available"

                    response.update({
                        str(entry[0].id): {
                            'author_name': entry[2],
                            'book_name': entry[0].name,
                            'book_type': entry[0].type,
                            'status': status
                        }
                    })
                for i in book_author_join.iter_pages(left_edge=2, right_edge=2, left_current=2, right_current=2):
                    num_list.append(i)

            return jsonify(
                data={key: response[key] for key in response.keys()},
                pages_lst=[value for value in num_list]
            )
        return jsonify(data=form.errors)
