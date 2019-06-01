from flask import render_template, url_for, redirect, jsonify
from app import app, db
from flask_login import current_user, login_required
from app.forms import New_Book, Choose_Author, Basic_search, Advanced_search_admnin, Update_book
import hashlib
from app.models import User, Author, Book, BookTypes, BookSeries, EntryWishlist, Log, EntryLog
from datetime import datetime, timedelta
import pytz


@app.route('/books')
@login_required
def books():
    if current_user.type != "admin":
        return render_template("page_403.html")
    new_book = New_Book()
    new_book.type_author.default = '1'
    new_book.type_exists.default = '1'
    new_book.process()
    choose_author = Choose_Author()
    basic_search_form = Basic_search()
    advanced_search_form = Advanced_search_admnin()
    update_book = Update_book()
    return render_template(
        "books.html",
        new_book=new_book,
        choose_author=choose_author,
        basic_search_form=basic_search_form,
        advanced_search_form=advanced_search_form,
        update_book_form=update_book
    )


@app.route('/add_new_book/', methods=["POST"])
@login_required
def add_new_book():
    if current_user.type != "admin":
        return render_template("page_403.html")
    new_book = New_Book()

    if new_book.validate_on_submit():
        book = Book.query.filter_by(name=new_book.name.data).first()
        author = None
        book_series = None
        if book:
            author = Author.query.filter_by(id=book.author_id).first()
            book_series = BookSeries.query.filter_by(
                book_id=book.id,
                series=new_book.series.data,
            ).first()

        if book and author and book_series:
            return jsonify(
                data={
                    'name': 'Book already exists !',
                    'type_string_field': 'Book already exists !',
                    'type': 'Book already exists !',
                    'author_first_name': 'Book already exists !',
                    'author_last_name': 'Book already exists !',
                    'series': 'Book already exists !',
                }
            )

        book_series_exists = BookSeries.query.filter_by(
            series=new_book.series.data,
        ).first()

        if book_series_exists:
            return jsonify(
                data={
                    'series': 'Series already exists !',
                }
            )

        if not author:
            author = Author(
                first_name=new_book.author_first_name.data,
                last_name=new_book.author_last_name.data,
                created_at=datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
                        pytz.timezone('Europe/Bucharest'))
            )
            db.session.add(author)
            db.session.commit()

        book_type= BookTypes(
            type_name=new_book.type.data,
            created_at=datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
                        pytz.timezone('Europe/Bucharest'))
        )
        db.session.add(book_type)
        db.session.commit()

        if not book:
            book = Book(
                name=new_book.name.data,
                count_free_books=1,
                count_total=1,
                author_id=author.id,
                type_id=book_type.id,
                created_at=datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
                        pytz.timezone('Europe/Bucharest'))
            )
            db.session.add(book)
            db.session.commit()

        if not book_series:
            book_series = BookSeries(
                book_id=book.id,
                series=new_book.series.data,
                status="available",
                created_at=datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
                        pytz.timezone('Europe/Bucharest'))

            )
        db.session.add(book_series)
        db.session.commit()

        return jsonify(data={
            'id': book_series.id,
            'code': 200
        })


        # print(
        #     new_book.name.data,
        #     new_book.type.data,
        #     new_book.type_string_field.data,
        #     new_book.series.data,
        #     new_book.author_first_name.data,
        #     new_book.author_last_name.data
        # )

    else:
        return jsonify(data=new_book.errors)


@app.route("/choose_author/", methods=["POST"])
@login_required
def choose_author():
    response = {}
    num_list = []
    form = Choose_Author()
    if form.validate_on_submit():
        name = ""
        if form.search_substring.data == False:
            name = form.author_name.data
        else:
            name = '%' + form.author_name.data + '%'

        authors = Author.query \
            .filter(Author.first_name.like(name) | (Author.last_name.like(name))) \
            .order_by(Author.first_name) \
            .paginate(
            per_page=3,
            page=form.page_nr.data,
            error_out=True
        )

        if authors:
            for entry in authors.items:
                response.update({
                    str(entry.id): {
                        'first_name': entry.first_name,
                        'last_name': entry.last_name,

                    }
                })
            for i in authors.iter_pages(left_edge=2, right_edge=2, left_current=2, right_current=2):
                num_list.append(i)

        return jsonify(
            data={key: response[key] for key in response.keys()},
            pages_lst=[value for value in num_list]
        )
    return jsonify(data=form.errors)


@app.route("/admin_dashboard_basic_search_book/", methods=["POST"])
@login_required
def admin_dashboard_basic_search_book():
    response = {}
    num_list = []

    if current_user.email:
        form = Basic_search()
        if form.validate_on_submit():
            name = ""
            if form.basic_search_substring.data == False:
                name = form.basic_search_name.data if form.basic_search_name.data != "all" else "%%"
            else:
                name = '%' + form.basic_search_name.data + '%'

            book_author_join = Book.query \
                .filter(Book.name.like(name)) \
                .join(Author, Book.author_id == Author.id) \
                .join(BookSeries, BookSeries.book_id==Book.id)\
                .order_by(Book.name) \
                .add_columns(Author.id, Author.first_name, Author.last_name, BookSeries.id) \
                .paginate(
                per_page=15,
                page=form.basic_page_number.data,
                error_out=True
            )

            if book_author_join:
                for entry in book_author_join.items:

                    book_series_available = BookSeries.query.filter_by(
                        book_id=entry[0].id,
                        status="available"
                    ).all()

                    book_series_unavailable = db.session\
                        .query(BookSeries)\
                        .filter(
                            (BookSeries.book_id==entry[0].id)
                            & ~(BookSeries.status=="available")
                        ).all()

                    for not_available in book_series_unavailable:
                        response.update({
                            str(not_available.id): {
                                'author_first_name': entry[2],
                                'author_last_name': entry[3],
                                'book_name': entry[0].name,
                                'book_type': BookTypes.query.filter_by(id=entry[0].type_id).first().type_name,
                                'status': not_available.status,
                                'book_series': not_available.series,
                            }
                        })

                    for available in book_series_available:
                        response.update({
                            str(available.id): {
                                'author_first_name': entry[2],
                                'author_last_name': entry[3],
                                'book_name': entry[0].name,
                                'book_type': BookTypes.query.filter_by(id=entry[0].type_id).first().type_name,
                                'status': available.status,
                                'book_series': available.series,
                            }
                        })

                for i in book_author_join.iter_pages(left_edge=2, right_edge=2, left_current=2, right_current=2):
                    num_list.append(i)

            return jsonify(
                data={key: response[key] for key in response.keys()},
                pages_lst=[value for value in num_list]
            )
        # print(form.errors)
        return jsonify(data=form.errors)


@app.route("/admin_dashboard_advanced_search_book/",methods=["POST"])
@login_required
def admin_dashboard_advanced_search_book():
    response = {}
    num_list = []

    if current_user.email:
        form = Advanced_search_admnin()
        if form.validate_on_submit():
            author_first_name = ""
            author_last_name = ""
            name = ""
            type = ""
            if form.search_substring.data == False:
                author_first_name = form.search_author_first_name.data if form.search_author_first_name.data else '%%'
                author_last_name = form.search_author_last_name.data if form.search_author_last_name.data else '%%'
                name = form.search_name.data if form.search_name.data else '%%'
                type = form.search_type.data if form.search_type.data else '%%'
            else:
                author_first_name = '%' + form.search_author_first_name.data + '%' if form.search_author_first_name.data else '%%'
                author_last_name = '%' + form.search_author_last_name.data + '%' if form.search_author_last_name.data else '%%'
                name = '%' + form.search_name.data + '%' if form.search_name.data else '%%'
                type = '%' + form.search_type.data + '%' if form.search_type.data else '%%'

            book_author_join = None

            if form.search_type.data:
                book_type = db.session() \
                    .query(BookTypes) \
                    .filter(
                    BookTypes.type_name.like(type)
                ).all()
                type_ids = []
                if book_type:
                    for t in book_type:
                        type_ids.append(t.id)

                book_series_status = ""
                if not form.only_unreturned.data and not form.only_available.data:
                    book_author_join = db.session() \
                        .query(Book) \
                        .filter(
                        (Book.type_id.in_(type_ids)) & (Book.name.like(name))
                    ) \
                        .join(Author, Book.author_id == Author.id) \
                        .filter(Author.first_name.like(author_first_name) & Author.last_name.like(author_last_name)) \
                        .join(BookSeries, BookSeries.book_id == Book.id) \
                        .order_by(Book.name) \
                        .add_columns(Author.id, Author.first_name, Author.last_name, BookSeries.id, BookSeries.series,
                                     BookSeries.status) \
                        .paginate(
                        per_page=15,
                        page=form.page_number.data,
                        error_out=True
                    )

                elif form.only_unreturned.data:
                    book_series_status= "taken"
                elif form.only_available.data:
                    book_series_status = "available"

                if book_series_status != "":
                    book_author_join = db.session() \
                        .query(Book) \
                        .filter(
                            (Book.type_id.in_(type_ids)) & (Book.name.like(name))
                        ) \
                        .join(Author, Book.author_id == Author.id) \
                        .filter(Author.first_name.like(author_first_name) & Author.last_name.like(author_last_name)) \
                        .join(BookSeries, BookSeries.book_id==Book.id)\
                        .filter(BookSeries.status==book_series_status)\
                        .order_by(Book.name) \
                        .add_columns(Author.id, Author.first_name, Author.last_name, BookSeries.id,BookSeries.series,BookSeries.status) \
                        .paginate(
                            per_page=15,
                            page=form.page_number.data,
                            error_out=True
                        )
            else:
                book_series_status = ""
                if not form.only_unreturned.data and not form.only_available.data:
                    book_author_join = db.session() \
                        .query(Book) \
                        .filter(Book.name.like(name)) \
                        .join(Author, Book.author_id == Author.id) \
                        .filter(Author.first_name.like(author_first_name) & Author.last_name.like(author_last_name)) \
                        .join(BookSeries, BookSeries.book_id == Book.id) \
                        .order_by(Book.name) \
                        .add_columns(Author.id, Author.first_name, Author.last_name, BookSeries.id, BookSeries.series,
                                     BookSeries.status) \
                        .paginate(
                        per_page=15,
                        page=form.page_number.data,
                        error_out=True
                    )

                elif form.only_unreturned.data:
                    book_series_status = "taken"
                elif form.only_available.data:
                    book_series_status = "available"

                if book_series_status != "":
                    book_author_join = db.session() \
                        .query(Book) \
                        .filter(Book.name.like(name)) \
                        .join(Author, Book.author_id == Author.id) \
                        .filter(Author.first_name.like(author_first_name) & Author.last_name.like(author_last_name)) \
                        .join(BookSeries, BookSeries.book_id == Book.id) \
                        .filter(BookSeries.status == book_series_status) \
                        .order_by(Book.name) \
                        .add_columns(Author.id, Author.first_name, Author.last_name, BookSeries.id,BookSeries.series,BookSeries.status) \
                        .paginate(
                        per_page=15,
                        page=form.page_number.data,
                        error_out=True
                    )

            if book_author_join:
                for entry in book_author_join.items:
                    # print(entry)

                    response.update({
                        str(entry[4]): {
                            'author_first_name': entry[2],
                            'author_last_name': entry[3],
                            'book_name': entry[0].name,
                            'book_type': BookTypes.query.filter_by(id=entry[0].type_id).first().type_name,
                            'status': entry[6],
                            'book_series': entry[5]
                        }
                    })
                for i in book_author_join.iter_pages(left_edge=2, right_edge=2, left_current=2, right_current=2):
                    num_list.append(i)

            return jsonify(
                data={key: response[key] for key in response.keys()},
                pages_lst=[value for value in num_list]
            )
        return jsonify(data=form.errors)


@app.route("/update_book/",methods=["POST"])
@login_required
def update_book():
    if current_user.type != "admin":
        return render_template("page_403.html")

    form = Update_book()
    if form.validate_on_submit():
        book_series = BookSeries.query.filter_by(id=form.update_book_series_id.data).first()
        book_old = Book.query.filter_by(id=book_series.book_id).first()
        type_old = BookTypes.query.filter_by(id=book_old.type_id).first()
        author_old = Author.query.filter_by(id=book_old.author_id).first()

        if book_series.series != form.update_book_series.data:
            book_series = form.update_book_series.data
            db.session.commit()

        if form.update_book_name.data != book_old.name:
            book_new = Book(
                name=form.update_book_name.data,
                count_total=1,
                count_free_books=1,
                type_id=book_old.type_id,
                author_id=book_old.author_id,
                created_at=datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
                    pytz.timezone('Europe/Bucharest'))
            )
            db.session.add(book_new)
            db.session.commit()
            book_series.book = book_new
            db.session.commit()
            print(book_new)
            if book_old.count_total == 1:
                db.session.delete(book_old)
                db.session.commit()

        if form.update_book_type.data != type_old.type_name:
            type_exists = BookTypes.query.filter_by(
                type_name=form.update_book_type.data
            ).first()

            if not type_exists:
                type_new = BookTypes(
                    type_name=form.update_book_type.data,
                    created_at=datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
                        pytz.timezone('Europe/Bucharest'))
                )
                db.session.add(type_new)
                db.session.commit()

                book_old.type_id = BookTypes.query.filter_by(
                    type_name=form.update_book_type.data
                ).first().id
                db.session.commit()
            else:
                book_old.type_id = type_exists.id
                db.session.commit()
            count = Book.query.filter_by(type_id=type_old.id).count()

            if count == 0:
                db.session.delete(type_old)
                db.session.commit()

        # if form.update_book_name.data != book_old.name\
        #     and (form.update_author_last_name.data != author_old.last_name
        #          or form.update_author_first_name.data != author_old.first_name
        #         )\
        #     and form.update_book_type != type_old.type_name:
        #
        #         print("Vai de veata mea!!")
        # elif form.update_book_name.data != book_old.name\
        #     and (form.update_author_last_name.data != author_old.last_name
        #          or form.update_author_first_name.data != author_old.first_name
        #         ):
        #         print("Vai de veata mea!!")
        # elif form.update_book_name.data != book_old.name and form.update_book_type != type_old.type_name:
        #         print("Vai de veata mea!!")



        # print(
        #     form.update_book_name.data,
        #     form.update_book_type.data,
        #     form.update_book_series.data,
        #     form.update_author_first_name.data,
        #     form.update_author_last_name.data,
        #     form.update_book_series_id.data
        # )
        return jsonify(
            data={
                'id': str(form.update_book_series_id.data)
            }
        )
    else:
        # print(form.errors)
        return jsonify(data=form.errors)