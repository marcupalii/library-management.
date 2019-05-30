from flask import render_template, url_for
from app import app
from app.models import Book, BookSeries, Author, Log, EntryLog, BookTypes
from flask_login import login_required, current_user
from flask import jsonify
from app.forms import Wishlist_settings
import re

@app.route("/books_log/page/<page>/focus=<book_id>/")
@login_required
def books_log(page, book_id):
    _email = current_user.email
    response = []
    num_list = []
    nr_of_pages = 1
    if _email:
        next_url = url_for('books_log', page=1, book_id=0)
        prev_url = url_for('books_log', page=1, book_id=0)

        book_log = Log.query.filter_by(id_user=current_user.id).first()

        if book_log:
            entry_log = EntryLog.query \
                .filter_by(id_log=book_log.id) \
                .order_by(EntryLog.created_at.desc()) \
                .paginate(per_page=15,
                          page=int(page),
                          error_out=True
                          )
            per_page = 15
            index = 1
            if int(page) > 1:
                index = (int(page) - 1) * per_page + 1

            if entry_log:
                for entry in entry_log.items:
                    book_series = BookSeries.query.filter_by(id=entry.id_book_series).first()
                    book = Book.query.filter_by(id=book_series.book_id).first()
                    author = Author.query.filter_by(id=book.author_id).first()

                    response.append([
                        index,
                        book.name,
                        BookTypes.query.filter_by(id=book.type_id).first().type_name,
                        author.first_name,
                        author.last_name,
                        re.search("(\d+-\d+-\d+\s+\d+:\d+:\d+)",str(entry.period_start)).groups(0)[0],
                        re.search("(\d+-\d+-\d+\s+\d+:\d+:\d+)",str(entry.period_end)).groups(0)[0],
                        entry.status,
                        entry.period_diff,
                        # re.search("([\sa-zA-Z0-9]*(\d+:\d+:\d+)?)",str(entry.period_diff)).groups(0)[0],
                        entry.id,
                    ])
                    index += 1

                next_url = url_for('books_log', page=entry_log.next_num, book_id=book_id) \
                    if entry_log.has_next else url_for('books_log', page=page, book_id=0)
                prev_url = url_for('books_log', page=entry_log.prev_num, book_id=book_id) \
                    if entry_log.has_prev else url_for('books_log', page=page, book_id=0)

                for i in entry_log.iter_pages(left_edge=2, right_edge=2, left_current=2, right_current=2):
                    num_list.append(i)

                if len(num_list) != 0:
                    nr_of_pages = num_list[-1]

        wishlist_settings = Wishlist_settings()
        wishlist_settings.setting_option.default = str(current_user.settings.wishlist_option)
        wishlist_settings.process()

        return render_template(
            'books_log.html',
            logs=response,
            id_user=current_user.id,
            next_url=next_url,
            prev_url=prev_url,
            num_list=num_list,
            nr_of_pages=nr_of_pages,
            wishlist_settings=wishlist_settings
        )


@app.route("/reserved_book/<book_id>/", methods=["GET"])
@login_required
def reserved_book(book_id):
    per_page = 15
    total_pages = 1
    log = Log.query.filter_by(id_user=current_user.id).first()
    total = EntryLog.query.filter_by(id_log=log.id).count()
    book_series = BookSeries.query.filter_by(book_id=book_id).all()

    if total > per_page:
        total_pages = total // per_page if total % per_page == 0 else (total // per_page) + 1

    for page in range(1, total_pages + 1):
        entry_log = EntryLog.query \
            .filter_by(id_log=log.id) \
            .order_by(EntryLog.created_at.desc()) \
            .paginate(per_page=15,
                      page=page,
                      error_out=True
            )

        for entry in entry_log.items:
            for book in book_series:
                if entry.id_book_series == book.id:
                    return jsonify({
                        "url": "/books_log/page/{}/focus={}".format(page, entry.id)
                    })
