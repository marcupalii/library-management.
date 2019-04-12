
from flask import render_template, request, url_for, redirect, abort
from app import app, login_manager
from app.models import User, Wishlist, EntryWishlist, Book, NextBook, BookSeries
from app import db
import hashlib
from app.forms import LoginForm
from flask_login import login_user, login_required, logout_user, current_user

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
@app.route('/home')
def home():
    return render_template("home.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return render_template("about.html")


@app.route("/wishlist_delete_entry/<entry_id>",methods=["GET"])
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
    return redirect(url_for("account"))



@app.route("/add_book_to_wishlist",methods=["POST"])
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

    return redirect(url_for("account"))


@app.route("/account")
@login_required
def account():
    _email = current_user.email
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
                _nextbook.append(_next_book.status)
                _nextbook.append(_next_book.id_series_book)

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
            _nextbook.append(_next_book.status)
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


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.type == "admin":
            return redirect(url_for('admin'))
        else:
            return redirect(url_for('account'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if user.password == hashlib.sha512(form.password.data.encode()).hexdigest():
                print("remember me =",form.remember.data)
                login_user(user, remember=form.remember.data)

                if user.type == "admin":
                    return redirect(url_for("admin"))
                else:
                    return redirect(url_for("account"))

        return '<h1>Invalid username or password</h1>'

    return render_template('login.html', form=form)


@app.route("/admin")
@login_required
def admin():
    return render_template("admin.html")
