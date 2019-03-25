
from flask import render_template, request, session, url_for, redirect, abort, current_app
from app import app, routine_thread
from app.models import User, Wishlist, EntryWishlist, Book, NextBook, BookSeries
from app import db
import hashlib

@app.before_first_request
def start_thread_function():
    if not routine_thread.is_alive():
        routine_thread.start()

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

    email_submitted = request.form.get("email")
    pass_submitted = request.form.get("pw")
    _user = User.query.filter_by(email=email_submitted).first()
    if _user:
        if _user.password == hashlib.sha512(pass_submitted.encode()).hexdigest():
            session["current_first_name"] = _user.first_name
            session["current_last_name"] = _user.last_name
            session["current_email"] = _user.email

            session["current_type"] = _user.type
            if _user.type == "admin":
                return redirect(url_for("admin"))
            else:
                return redirect(url_for("account"))


    return render_template("about.html")


@app.route("/logout")
def logout():
    session.pop("current_first_name", None)
    session.pop("current_last_name", None)
    session.pop("current_email", None)
    session.pop("current_type", None)
    return render_template("about.html")


@app.route("/wishlist_delete_entry/<entry_id>",methods=["GET"])
def wishlist_delete_entry(entry_id):
    _user = User.query.filter_by(email=session.get("current_email",None)).first()
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
    return redirect(url_for("account"))


# @app.route("/deny_book/<entry_id>", methods=["GET"])
# def deny_book(entry_id):
#     _user = User.query.filter_by(username=session.get("current_user", None)).first()
#     if _user:
#         pass
#
#     return redirect(url_for("account"))
#
#
# @app.route("/accept_book/<entry_id>", methods=["GET"])
# def accept_book(entry_id):
#     _user = User.query.filter_by(email=session.get("current_email",None)).first()
#     if _user:
#         pass
#
#     return redirect(url_for("account"))


@app.route("/add_book_to_wishlist",methods=["POST"])
def add_book_to_wishlist():
    _name = request.form.get("name")
    _period = request.form.get("period")
    _rank = int(request.form.get("rank"))
    _book = Book.query.filter_by(name=_name).first()
    if _book:

        _user = User.query.filter_by(email=session.get("current_email",None)).first()
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

    return redirect(url_for("account"))


@app.route("/account")
def account():
    _email = session.get("current_email", None)
    _wishlist = []
    _nextbook = []
    rank = -1
    if _email:
        _user = User.query.filter_by(email=_email).first()

        wishList = _user.wishlist
        _next_book = _user.next_book

        response = []

        if _next_book.status == "Checking":
            _entry = EntryWishlist.query.filter_by(
                id_wishlist=wishList.id,
                id_book=_next_book.id_book,
                period=_next_book.period
            ).first()
            if _entry:
                rank = _entry.rank
                _next_book.status = "Pending"
                db.session.delete(_entry)
                db.session.commit()

                _book = Book.query.filter_by(id=_next_book.id_book).first()
                _nextbook.append(_book.name)
                _nextbook.append(_book.type)
                _nextbook.append(_next_book.period)
                _nextbook.append(_next_book.id)
            else:

                _next_book.status = "None"
                _next_book.period = 0

                _book = Book.query.filter_by(id=_next_book.id_book).first()
                _book.count_free_books += 1

                _series_book = BookSeries.query.filter_by(id=_next_book.id_series_book).first()
                _series_book.status = "available"
                db.session.commit()

        elif _next_book.status == "Pending":
        # check if the book is acepting within 5 hours
            _book = Book.query.filter_by(id=_next_book.id_book).first()
            _nextbook.append(_book.name)
            _nextbook.append(_book.type)
            _nextbook.append(_next_book.period)
            _nextbook.append(_next_book.id_series_book)



        _entry_wishlist = wishList.entry_wishlists

        for _entry in _entry_wishlist:
            if rank != -1 and _entry.rank > rank:

                _entry.rank -= 1
                db.session.commit()
            _book = Book.query.filter_by(id=_entry.id_book).first()
            response.append([_entry.rank, _book.name, _book.type, _entry.period, _entry.id])


        # _next_book.status= ["None","Pending","NoNeed","Checking"]
        # next_nook need id_book field sau series_book_field

        _wishlist = [sorted(response, key=lambda l: l[0])].copy()

    return render_template("account.html", wishlist=_wishlist, nextbook=_nextbook)


@app.route("/admin")
def admin():
    return render_template("admin.html")
