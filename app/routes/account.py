
from flask import render_template, request, url_for, redirect
from app import app, db
from app.models import User, EntryWishlist, Book, BookSeries, Notifications, Author, Log, EntryLog
from app.forms import Search, Wishlist_form, Reserved_book_date
from flask_login import login_required, current_user
from flask import jsonify


@app.route("/account")
@login_required
def account():
    _email = current_user.email

    if _email:
        _user = User.query.filter_by(email=_email).first()

        form = Search(search_by_name=False, search_by_type=False, search_by_author=False)
        wishlist_form = Wishlist_form()
        reserved_book_date = Reserved_book_date()
        nr = EntryWishlist.query.filter_by(id_wishlist=_user.wishlist.id).count()

        if nr:
            wishlist_form.rank.label = "Rank({}-{})".format(1, nr + 1)
        else:
            wishlist_form.rank.label = "Rank({})".format(1)

        return render_template(
            'account.html',
            form=form,
            wishlist_form=wishlist_form,
            reserved_book_date=reserved_book_date
        )
    else:
        return redirect(url_for('about'))


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

                new_entry = EntryWishlist(wishlist=wishlist, id_book=book.id, rank=form.rank.data,
                                          period=form.days_number.data)

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
                .join(EntryWishlist, EntryWishlist.id_book != Book.id) \
                .filter(EntryWishlist.id_wishlist==current_user.wishlist.id,)\
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
                        id_book=entry[0].id
                    ).first()
                    book_series = BookSeries.query.filter_by(book_id=entry[0].id).all()

                    status = ""
                    for series in book_series:
                        entry_log = EntryLog.query.filter_by(
                            id_book_series=series.id,
                            status="Reserved"
                        ).all()
                        if entry_log:
                            status = "Reserved"
                            break

                    if status == "":
                        if entry_wishlist:
                            status = "Already in wishlist"
                        elif entry[0].count_free_books <= 3:
                            status = "Unavailable"
                        else:
                            status = "Available"
                    print(status)
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


@app.route("/add_to_reserved/", methods=["POST"])
@login_required
def add_to_reserved():
    if current_user.email:
        print("router:add_to_reserved")
        form = Reserved_book_date()
        if form.validate_on_submit():

            book_log = Log.query.filter_by(id_user=current_user.id).first()
            if not book_log:
                book_log = Log(id_user=current_user.id)
                db.session.add(book_log)
                db.session.commit()
            book_log = Log.query.filter_by(id_user=current_user.id).first()
            fmt = "%Y-%m-%d"
            # date_start = datetime.datetime.strptime(form.startdate.data, fmt)\
            #     .replace(tzinfo=pytz.UTC)\
            #     .astimezone(pytz.timezone('Europe/Bucharest'))
            #
            # date_end = datetime.datetime.strptime(form.enddate.data, fmt) \
            #     .replace(tzinfo=pytz.UTC) \
            #     .astimezone(pytz.timezone('Europe/Bucharest'))

            entry_log = EntryLog(
                id_log=book_log.id,
                id_book_series=BookSeries.query.filter_by(book_id=form.book_id_reserved.data).first().id,
                status="Reserved",
                period_start=form.startdate.data,
                period_end=form.enddate.data
            )
            db.session.add(entry_log)
            db.session.commit()

            return jsonify(data="succes")
        print(form.errors)
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

