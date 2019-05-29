from flask import render_template, request, url_for, redirect
from app import app, db
from app.models import User, EntryWishlist, Book, BookSeries, Notifications, Author, Log, EntryLog, User_settings
from app.forms import Basic_search, Advanced_search, Wishlist_form, Reserved_book_date, Wishlist_settings
from flask_login import login_required, current_user
from flask import jsonify
from datetime import datetime
import pytz
import re

@app.route('/user_trust_coeff_statistics/', methods=["GET"])
@login_required
def user_trust_coeff_statistics():
    return jsonify({
        'coeff': current_user.trust_coeff
    })


@app.route('/book_type_statistics/', methods=["GET"])
@login_required
def book_type_statistics():
    types = {}
    log = Log.query.filter_by(id_user=current_user.id).first()
    entry_logs = None
    if log:
        entry_logs = EntryLog.query.filter_by(id_log=log.id).all()

    if entry_logs:
        for entry_log in entry_logs:
            book_series = BookSeries.query.filter_by(id=entry_log.id_book_series).first()
            book = Book.query.filter_by(id=book_series.book_id).first()
            if book.type not in types.keys():
                types.update({book.type: 1})
            else:
                types[book.type] += 1

    types = {item[0]: item[1] for item in sorted(types.items(), key=lambda kv: kv[1])}
    response_type = {}
    if len(types) > 2:
        for k in types.keys():
            if len(response_type) == 2:
                response_type.update({'others': 0})
            elif len(response_type) == 3:
                response_type['others'] += types[k]
            else:
                response_type.update({k: types[k]})

    return jsonify({
        "types": response_type if len(response_type) != 0 else types
    })


@app.route("/account")
@login_required
def account():
    advanced_search_form = Advanced_search(search_by_name=False, search_by_type=False, search_by_author=False)
    basic_search_form = Basic_search()
    wishlist_form = Wishlist_form()
    reserved_book_date = Reserved_book_date()
    nr = EntryWishlist.query.filter_by(id_wishlist=current_user.wishlist.id).count()

    if nr:
        wishlist_form.rank.label = "Rank({}-{})".format(1, nr + 1)
    else:
        wishlist_form.rank.label = "Rank({})".format(1)

    wishlist_form.process()
    wishlist_settings = Wishlist_settings()
    wishlist_settings.setting_option.default = str(current_user.settings.wishlist_option)
    wishlist_settings.process()

    print(wishlist_form.rank.label)
    return render_template(
        'account.html',
        advanced_search_form=advanced_search_form,
        basic_search_form=basic_search_form,
        wishlist_form=wishlist_form,
        reserved_book_date=reserved_book_date,
        wishlist_settings=wishlist_settings
    )


@app.route("/add_to_wishlist/", methods=['POST'])
@login_required
def add_to_wishlist():
    if current_user.email:
        form = Wishlist_form()
        if form.validate_on_submit():

            book = Book.query.filter_by(id=form.book_id.data).first()
            if book:
                wishlist = current_user.wishlist

                entrywishlist = wishlist.entry_wishlists
                for entry in entrywishlist:

                    if entry.rank >= form.rank.data:
                        entry.rank += 1
                        db.session.commit()

                new_entry = EntryWishlist(
                    wishlist=wishlist,
                    id_book=book.id,
                    rank=form.rank.data,
                    created_at=datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
                        pytz.timezone('Europe/Bucharest')),
                    period=form.days_number.data
                )

                db.session.add(new_entry)
                db.session.commit()
            nr = EntryWishlist.query.filter_by(id_wishlist=current_user.wishlist.id).count()
            return jsonify(data=nr + 1)
        return jsonify(data=form.errors)


@app.route("/basic_search_book/", methods=['POST'])
@login_required
def basic_search_book():
    response = {}
    num_list = []

    if current_user.email:
        form = Basic_search()
        if form.validate_on_submit():
            name = ""
            if form.basic_search_substring.data == False:
                name = form.basic_search_name.data
            else:
                name = '%' + form.basic_search_name.data + '%'

            book_author_join = Book.query \
                .filter(Book.name.like(name)) \
                .join(Author, Book.author_id == Author.id) \
                .order_by(Book.name) \
                .add_columns(Author.id, Author.name) \
                .paginate(
                per_page=15,
                page=form.basic_page_number.data,
                error_out=True
            )

            if book_author_join:
                for entry in book_author_join.items:
                    entry_wishlist = EntryWishlist.query.filter_by(
                        id_wishlist=current_user.wishlist.id,
                        id_book=entry[0].id
                    ).first()
                    book_series = BookSeries.query.filter_by(book_id=entry[0].id).all()

                    status = ""
                    period_diff = "0 days 00:00:00"
                    log = Log.query.filter_by(id_user=current_user.id).first()
                    if log:
                        for series in book_series:
                            entry_log = EntryLog.query.filter_by(
                                id_book_series=series.id,
                                id_log=log.id
                            ).first()
                            if entry_log:
                                status = entry_log.status
                                period_diff = entry_log.period_diff
                                break

                    if status == "":
                        if entry_wishlist:
                            status = "Already in wishlist"
                        elif entry[0].count_free_books <= 3:
                            status = "Unavailable"
                        else:
                            status = "Available"
                    response.update({
                        str(entry[0].id): {
                            'author_name': entry[2],
                            'book_name': entry[0].name,
                            'book_type': entry[0].type,
                            'status': status,
                            'period_diff': period_diff
                        }
                    })
                for i in book_author_join.iter_pages(left_edge=2, right_edge=2, left_current=2, right_current=2):
                    num_list.append(i)

            return jsonify(
                data={key: response[key] for key in response.keys()},
                pages_lst=[value for value in num_list]
            )
        return jsonify(data=form.errors)


@app.route("/advanced_search_book/", methods=['POST'])
@login_required
def advanced_search_book():
    response = {}
    num_list = []

    if current_user.email:
        form = Advanced_search()
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

            book_author_join = None

            if form.only_available.data:
                entry_wishlist = EntryWishlist.query.filter_by(id_wishlist=current_user.wishlist.id).all()
                ids_wishlist = []
                for entry in entry_wishlist:
                    ids_wishlist.append(entry.id_book)

                ids_current_books = []
                log = Log.query.filter_by(id_user=current_user.id).first()
                if log:
                    entry_logs = db.session().query(EntryLog).filter(
                        (EntryLog.id_log == log.id)
                        & ~(EntryLog.status.in_(["Returned","Reserved expired"]))
                    ).all()

                    for entry in entry_logs:
                        ids_current_books.append(BookSeries.query.filter_by(id=entry.id_book_series).first().book_id)

                book_author_join = db.session() \
                    .query(Book) \
                    .filter(
                    ~(Book.id.in_(ids_wishlist))
                    & (Book.type.like(type))
                    & (Book.name.like(name))
                    & ~(Book.id.in_(ids_current_books))
                    & (Book.count_free_books > 3)
                ) \
                    .join(Author, Book.author_id == Author.id) \
                    .filter(Author.name.like(author)) \
                    .order_by(Book.name) \
                    .add_columns(Author.id, Author.name) \
                    .paginate(
                    per_page=15,
                    page=form.page_number.data,
                    error_out=True
                )

            elif form.exclude_wishlist.data and form.exclude_current_book.data:
                entry_wishlist = EntryWishlist.query.filter_by(id_wishlist=current_user.wishlist.id).all()
                ids_wishlist = []
                for entry in entry_wishlist:
                    ids_wishlist.append(entry.id_book)

                ids_current_books = []
                log = Log.query.filter_by(id_user=current_user.id).first()
                if log:
                    entry_logs = db.session().query(EntryLog).filter(
                        (EntryLog.id_log == log.id)
                        & ~(EntryLog.status.in_(["Returned","Reserved expired"]))
                    ).all()

                    for entry in entry_logs:
                        ids_current_books.append(BookSeries.query.filter_by(id=entry.id_book_series).first().book_id)

                book_author_join = db.session() \
                    .query(Book) \
                    .filter(
                    ~(Book.id.in_(ids_wishlist))
                    & (Book.type.like(type))
                    & (Book.name.like(name))
                    & ~(Book.id.in_(ids_current_books))
                ) \
                    .join(Author, Book.author_id == Author.id) \
                    .filter(Author.name.like(author)) \
                    .order_by(Book.name) \
                    .add_columns(Author.id, Author.name) \
                    .paginate(
                    per_page=15,
                    page=form.page_number.data,
                    error_out=True
                )
            elif form.exclude_wishlist.data:
                entry_wishlist = EntryWishlist.query.filter_by(id_wishlist=current_user.wishlist.id).all()
                ids = []
                for entry in entry_wishlist:
                    ids.append(entry.id_book)

                book_author_join = db.session() \
                    .query(Book) \
                    .filter(~(Book.id.in_(ids)) & (Book.type.like(type)) & Book.name.like(name)) \
                    .join(Author, Book.author_id == Author.id) \
                    .filter(Author.name.like(author)) \
                    .order_by(Book.name) \
                    .add_columns(Author.id, Author.name) \
                    .paginate(
                    per_page=15,
                    page=form.page_number.data,
                    error_out=True
                )
            elif form.exclude_current_book.data:
                ids_current_books = []
                log = Log.query.filter_by(id_user=current_user.id).first()
                if log:
                    entry_logs = db.session().query(EntryLog).filter(
                        (EntryLog.id_log == log.id)
                        & ~(EntryLog.status.in_(["Returned","Reserved expired"]))
                    ).all()
                    for entry in entry_logs:
                        ids_current_books.append(BookSeries.query.filter_by(id=entry.id_book_series).first().book_id)

                book_author_join = db.session() \
                    .query(Book) \
                    .filter(
                    (Book.type.like(type))
                    & (Book.name.like(name))
                    & ~(Book.id.in_(ids_current_books))
                ) \
                    .join(Author, Book.author_id == Author.id) \
                    .filter(Author.name.like(author)) \
                    .order_by(Book.name) \
                    .add_columns(Author.id, Author.name) \
                    .paginate(
                    per_page=15,
                    page=form.page_number.data,
                    error_out=True
                )
            else:
                book_author_join = Book.query \
                    .filter(Book.name.like(name) & (Book.type.like(type))) \
                    .join(Author, Book.author_id == Author.id) \
                    .filter(Author.name.like(author)) \
                    .order_by(Book.name) \
                    .add_columns(Author.id, Author.name) \
                    .paginate(
                    per_page=15,
                    page=form.page_number.data,
                    error_out=True
                )

            if book_author_join:
                for entry in book_author_join.items:
                    entry_wishlist = EntryWishlist.query.filter_by(
                        id_wishlist=current_user.wishlist.id,
                        id_book=entry[0].id
                    ).first()
                    book_series = BookSeries.query.filter_by(book_id=entry[0].id).all()

                    status = ""
                    period_diff = "0 days 00:00:00"
                    log = Log.query.filter_by(id_user=current_user.id).first()
                    if log:
                        for series in book_series:
                            entry_log = EntryLog.query.filter_by(
                                id_book_series=series.id,
                                id_log=log.id
                            ).first()
                            if entry_log:
                                status = entry_log.status
                                period_diff = entry_log.period_diff

                    if status == "":
                        if entry_wishlist:
                            status = "Already in wishlist"
                        elif entry[0].count_free_books <= 3:
                            status = "Unavailable"
                        else:
                            status = "Available"
                    response.update({
                        str(entry[0].id): {
                            'author_name': entry[2],
                            'book_name': entry[0].name,
                            'book_type': entry[0].type,
                            'status': status,
                            'period_diff': period_diff
                        }
                    })
                for i in book_author_join.iter_pages(left_edge=2, right_edge=2, left_current=2, right_current=2):
                    num_list.append(i)

            return jsonify(
                data={key: response[key] for key in response.keys()},
                pages_lst=[value for value in num_list]
            )
        return jsonify(data=form.errors)


@app.route("/add_to_reserved/", methods=["POST"])
@login_required
def add_to_reserved():
    if current_user.email:
        form = Reserved_book_date()
        if form.validate_on_submit():
            book_log = Log.query.filter_by(id_user=current_user.id).first()
            if not book_log:
                book_log = Log(
                    id_user=current_user.id,
                    created_at=datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
                        pytz.timezone('Europe/Bucharest'))

                )
                db.session.add(book_log)
                db.session.commit()
            book_log = Log.query.filter_by(id_user=current_user.id).first()

            time_now = datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
                pytz.timezone('Europe/Bucharest'))
            period_start = time_now
            diff = form.end_date.data-form.start_date.data

            period_end = time_now+(diff)
            entry_log = EntryLog(
                id_log=book_log.id,
                id_book_series=BookSeries.query.filter_by(book_id=form.book_id_reserved.data).first().id,
                status="Reserved",
                period_start=period_start,
                period_end=period_end,
                created_at=datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
                    pytz.timezone('Europe/Bucharest')),
                period_diff=str(period_end - period_start)
            )
            db.session.add(entry_log)
            db.session.commit()

            return jsonify(data="succes")

        return jsonify(data=form.errors)


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


@app.route("/mark_notification_read/", methods=['POST'])
@login_required
def mark_notification_read():
    _email = current_user.email

    if _email:
        _user = User.query.filter_by(email=_email).first()
        _notification = Notifications.query.filter_by(
            id_user=_user.id,
            id=int(request.data.decode().split("=")[1])
        ).first()
        if _notification:
            _notification.status = "read"
            db.session.commit()

        return render_template("layout.html", id_user=current_user.id)


@app.route("/save_settings/", methods=["POST"])
@login_required
def save_settings():
    form = Wishlist_settings()
    if form.validate_on_submit():
        settings = User_settings.query.filter_by(id_user=current_user.id).first()
        settings.wishlist_option = int(form.setting_option.data)
        db.session.commit()
        return jsonify({
            'option': form.setting_option.data
        })
    return jsonify(data=form.errors)


@app.route("/books_count/", methods=["GET"])
@login_required
def books_count():

    # log = Log.query.filter_by(id_user=current_user.id).first()
    # total = EntryLog.query.filter_by(
    #     id_log=log.id
    # ).count()
    # entry_logs = EntryLog.query.filter_by(
    #     id_log=log.id,
    #     status="Returned"
    # )
    # count_late = 0
    # count_in_time = 0
    # if entry_logs:
    #     for entry in entry_logs:
    #         if re.search("-",str(entry.period_diff)):
    #                 count_late += 1
    #         else:
    #             count_in_time += 1

    return jsonify({
        "total": 0,
        "count_late" :0,
        "count_in_time":0
    })
