from flask import render_template, url_for, redirect, abort
from app import app, db
from app.models import User, EntryWishlist, Book, Author
from flask_login import login_required, current_user
from flask import jsonify
from app.forms import Wishlist_settings

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
            return abort(401)

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
                    book.type,
                    author.name,
                    entry.period,
                    entry.created_at,
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

        return render_template(
            'wishlist.html',
            wishlist=response,
            id_user=current_user.id,
            next_url=next_url,
            prev_url=prev_url,
            num_list=num_list,
            nr_of_pages=nr_of_pages,
            wishlist_settings=wishlist_settings
        )


@app.route("/wishlist_book/<book_id>/", methods=["GET"])
@login_required
def wishlist_book(book_id):
    book = EntryWishlist.query.filter_by(id_book=book_id).first()
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

