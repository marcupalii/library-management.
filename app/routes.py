
from flask import render_template, request, session, url_for, redirect, abort, current_app
from app import app
from app.models import User, Wishlist, EntryWishlist, Book, NextBook
from helpers import _wishlist_delete_entry,_add_book_to_wishlist, getNextBook

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

#
# def send_async_email(app, msg):
#     n, p = msg
#     with app.app_context():
#         while True:
#             _user = User.query.filter_by(username=n).first()
#             print(_user)
#
# def send_email(name,passw):
#     msg = (name,passw)
#     Thread(target=send_async_email,
#            args=(current_app._get_current_object(), msg)).start()


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
    if _user:
        if _user.password == hashlib.sha512(pass_submitted.encode()).hexdigest():
            session["current_user"] = _user.username
            session["current_type"] = _user.type
            # send_email(_user.username,_user.type)
            # print(session.get("current_type"),session.get("current_type"))
            return render_template("account.html")

    return render_template("about.html")


@app.route("/logout")
def logout():
    session.pop("current_user", None)
    session.pop("current_type", None)
    return render_template("about.html")


def getWishlist(user_id):
    _wishLists = Wishlist.query.filter_by(id_user=user_id)
    res = []
    if _wishLists:
        print(_wishLists)
        for _wishList in _wishLists:
            _entryWishList = _wishList.entrywishlist
            if _entryWishList:
                _book = Book.query.filter_by(id=_entryWishList.id_book).first()
                if _book:
                    res.append([_entryWishList.rank,_book.name,_book.type,_entryWishList.period,_entryWishList.id_wishlist])

    return [sorted(res,key=lambda l: l[0])]


@app.route("/wishlist_delete_entry/<entry_id>",methods=["GET"])
def wishlist_delete_entry(entry_id):
    _user = User.query.filter_by(username=session.get("current_user",None)).first()
    if _user:
        _wishlist = Wishlist.query.filter_by(id=entry_id).first()
        if _wishlist.id_user == _user.id:
            _wishlist_delete_entry(entry_id,_wishlist.entrywishlist,_user.id)
        else:
            return abort(401)
    return redirect(url_for("account"))


@app.route("/deny_book/<entry_id>", methods=["GET"])
def deny_book(entry_id):
    _user = User.query.filter_by(username=session.get("current_user", None)).first()
    if _user:
        pass

    return redirect(url_for("account"))


@app.route("/accept_book/<entry_id>", methods=["GET"])
def accept_book(entry_id):
    _user = User.query.filter_by(username=session.get("current_user",None)).first()
    if _user:
        # _next_book = NextBook.query.filter_by(id=entry_id).first()
        # if _next_book.id_user == _user.id:
        #     _wishlists = Wishlist.query.filter_by(id_user=_user.id)
        #     for _wishlist in _wishlists:
        #         if _wishlist:
        #             _entrywishlist = _wishlist.entrywishlist
        #             if _entrywishlist.id_book == _next_book.id_book and _entrywishlist.period == _next_book.period:
        #                 _next_book.status = "Accepted"
        #             else:
        #                 _next_book.status = "None"
        # else:
        #     return abort(401)
        pass
    return redirect(url_for("account"))


@app.route("/add_book_to_wishlist",methods=["POST"])
def add_book_to_wishlist():
    _name = request.form.get("name")
    _period = request.form.get("period")
    _rank = request.form.get("rank")
    _book = Book.query.filter_by(name=_name).first()
    if _book:
        _add_book_to_wishlist(_book,session.get("current_user",None),_period,_rank)
    else:
        return abort(401)

    return redirect(url_for("account"))




@app.route("/account")
def account():
    _user_curr = session.get("current_user", None)
    _wishlist = []
    _nextbook = []
    if _user_curr:
        _user = User.query.filter_by(username=_user_curr).first()
        _wishlist = getWishlist(_user.id)   # +=  ????

        res_nextbook = getNextBook(_user.id)
        if res_nextbook:
            _book = Book.query.filter_by(id=res_nextbook.id_book)
            _nextbook.append(_book.name)
            _nextbook.append(_book.type)
            _nextbook.append(res_nextbook.period)
            _nextbook.append(res_nextbook.id)

    return render_template("account.html", wishlist=_wishlist, nextbook=_nextbook)

# @app.route("/return_book",methods=["POST"])
# def return_book():
#     _user_name = request.form.get("user")
#     _book_name = request.form.get("book")
#
#     _user_curr = session.get("current_user", None)
#     if _user_curr:
#         _user = User.query.filter_by(username=_user_curr).first()
#         if _user.type =="admin":
#
#         else:
#             return abort(401)

@app.route("/admin")
def admin():
    return render_template("admin.html")
