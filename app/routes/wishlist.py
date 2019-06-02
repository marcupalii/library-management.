from flask import render_template, request, url_for, redirect, abort
from app import app, db
from app.models import User, EntryWishlist, Log, Book, Author, NextBook, EntryLog, BookTypes
from flask_login import login_required, current_user
from flask import jsonify
from app.forms import Wishlist_settings, Accept_next_book
from datetime import datetime, timedelta
import pytz
from app import not_found
import re


@app.route("/wishlist_delete_entry/<entry_id>", methods=["GET"])
@login_required
def wishlist_delete_entry(entry_id):
    user = User.query.filter_by(email=current_user.email).first()
    per_page = 15
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

            return not_found("nu exista in entrywishlist id="+entry_id)

    total = EntryWishlist.query.filter_by(id_wishlist=current_user.wishlist.id).count()
    page = 1
    total_pages = 1

    if rank > per_page:
        page = rank // per_page if rank % per_page == 0 else (rank // per_page) + 1

    if total > total_pages:
        total_pages = total // per_page if total % per_page == 0 else (total // per_page) + 1

    if page > total_pages:
        page = total_pages
    return redirect(url_for("wishlist", page=page, book_id=0))


@app.route("/wishlist/page/<page>/focus=<book_id>/")
@login_required
def wishlist(page, book_id):
    _email = current_user.email
    response = []
    num_list = []
    nr_of_pages = 1
    if _email:

        next_url = url_for('wishlist', page=1, book_id=book_id)
        prev_url = url_for('wishlist', page=1, book_id=book_id)

        user = User.query.filter_by(email=_email).first()

        entry_wishlist = EntryWishlist.query \
            .filter_by(id_wishlist=user.wishlist.id) \
            .order_by(EntryWishlist.rank.asc()) \
            .paginate(per_page=15,
                      page=int(page),
                      error_out=True
                      )

        if entry_wishlist:
            for entry in entry_wishlist.items:
                book = Book.query.filter_by(id=entry.id_book).first()
                author = Author.query.filter_by(id=book.author_id).first()
                response.append([
                    entry.rank,
                    book.name,
                    BookTypes.query.filter_by(id=book.type_id).first().type_name,
                    author.first_name,
                    author.last_name,
                    entry.period,
                    re.search("(\d+-\d+-\d+\s+\d+:\d+:\d+)", str(entry.updated_at)).groups(0)[0],
                    entry.id
                ])

            next_url = url_for('wishlist', page=entry_wishlist.next_num, book_id=book_id) \
                if entry_wishlist.has_next else url_for('wishlist', page=page, book_id=0)
            prev_url = url_for('wishlist', page=entry_wishlist.prev_num, book_id=book_id) \
                if entry_wishlist.has_prev else url_for('wishlist', page=page, book_id=0)

            for i in entry_wishlist.iter_pages(left_edge=2, right_edge=2, left_current=2, right_current=2):
                num_list.append(i)

            if len(num_list) != 0:
                nr_of_pages = num_list[-1]

        wishlist_settings = Wishlist_settings()
        wishlist_settings.setting_option.default = str(current_user.settings.wishlist_option)
        wishlist_settings.process()

        next_book_query = NextBook.query.filter_by(
            id_user=current_user.id,
            status="Pending"
        ).first()
        next_book = []
        if next_book_query:
            book = Book.query.filter_by(id=next_book_query.id_book).first()
            author = Author.query.filter_by(id=book.author_id).first()
            period_start = next_book_query.updated_at + timedelta(hours=3)
            period_end = period_start + timedelta(days=next_book_query.period)
            next_book = [
                next_book_query.id,
                book.name,
                BookTypes.query.filter_by(id=book.type_id).first().type_name,
                author.first_name,
                author.last_name,
                re.search("(\d+-\d+-\d+\s+\d+:\d+:\d+)", str(period_start)).groups(0)[0],
                re.search("(\d+-\d+-\d+\s+\d+:\d+:\d+)", str(period_end)).groups(0)[0],

            ]
        next_book_form = Accept_next_book()
        return render_template(
            'wishlist.html',
            wishlist=response,
            id_user=current_user.id,
            next_url=next_url,
            prev_url=prev_url,
            num_list=num_list,
            nr_of_pages=nr_of_pages,
            wishlist_settings=wishlist_settings,
            next_book=next_book,
            next_book_form=next_book_form
        )


@app.route("/wishlist_book/<book_id>/", methods=["GET"])
@login_required
def wishlist_book(book_id):
    book = EntryWishlist.query.filter_by(id_book=book_id).first()
    if not book:
        return not_found("nu exista cartea")
    per_page = 15
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
        "url": "/wishlist/page/{}/focus={}".format(page, book.rank),
        "rank": book.rank
    })


@app.route("/accept_next_book/", methods=["POST"])
@login_required
def accept_next_book():
    form = Accept_next_book()
    if form.validate_on_submit():
        next_book = NextBook.query.filter_by(
            id=form.next_book_id.data,
            id_user=current_user.id
        ).first()
        if not next_book:
            return not_found("nu exista cartea")
        log = Log.query.filter_by(id_user=current_user.id).first()
        if not log:
            log = Log(
                id_user=current_user.id,
                created_at=datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
                    pytz.timezone('Europe/Bucharest'))
            )
            db.session.add(log)
            db.session.commit()
        log = Log.query.filter_by(id_user=current_user.id).first()
        period_start = datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
            pytz.timezone('Europe/Bucharest'))
        period_end = period_start + timedelta(days=next_book.period)
        entry_log = EntryLog(
            id_log=log.id,
            id_book_series=next_book.id_series_book,
            status="Unreturned",
            period_start=period_start,
            period_end=period_end,
            period_diff=period_end - period_start,
            created_at=period_start
        )
        next_book.status = "Have one"
        next_book.period = 0

        db.session.add(entry_log)
        db.session.commit()
        return jsonify(data={'id': 1}, status=200)
    return jsonify(data=form.errors)
