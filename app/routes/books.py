from flask import render_template, url_for, redirect, jsonify
from app import app, db
from flask_login import current_user, login_required
from app.forms import New_Book, Choose_Author, Basic_search, Advanced_search_admnin, Update_book
import hashlib
from app.models import User, Author, Book, BookTypes, BookSeries, NextBook, EntryWishlist, Log, EntryLog
from datetime import datetime, timedelta
import pytz
from app import not_found
import time
import re
from sqlalchemy import desc


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
        book_type = None
        author = None
        book_series = None

        if new_book.type_exists.data == "1":
            book_type = BookTypes.query.filter_by(id=str(new_book.type.data)).first()
            if not book_type:
                return jsonify(
                    data={
                        'type': 'Type do not exists !',
                    }
                )
        else:
            book_type = BookTypes.query.filter_by(type_name=new_book.type_string_field.data).first()
            if book_type:
                return jsonify(
                    data={
                        'type_string_field': 'Type already exists !',
                    }
                )
        if new_book.type_author.data == '1':
            author = Author.query.filter_by(
                first_name=new_book.author_first_name.data,
                last_name=new_book.author_last_name.data,
            ).first()
            if author:
                return jsonify(
                    data={
                        'author_first_name': 'Author already exists !',
                        'author_last_name': 'Author already exists !',
                    }
                )
        else:
            author = Author.query.filter_by(
                first_name=new_book.author_first_name.data,
                last_name=new_book.author_last_name.data,
            ).first()
            if not author:
                return jsonify(
                    data={
                        'author_first_name': 'Author does not exists !',
                        'author_last_name': 'Author does not exists !',
                    }
                )

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

        if not book_type:
            book_type = BookTypes(
                type_name=new_book.type_string_field.data,
                created_at=datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
                    pytz.timezone('Europe/Bucharest'))
            )
            db.session.add(book_type)
            db.session.commit()

        db.session.refresh(author)
        db.session.refresh(book_type)

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

        db.session.refresh(book)
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

    else:
        print(new_book.errors)
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
            per_page=15,
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
    response = []
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
                .join(BookSeries, BookSeries.book_id == Book.id) \
                .order_by(desc(BookSeries.status)) \
                .add_columns(Author.id, Author.first_name, Author.last_name, BookSeries.id) \
                .paginate(
                per_page=15,
                page=form.basic_page_number.data,
                error_out=True
            )

            if book_author_join:
                for entry in book_author_join.items:
                    book_series = BookSeries.query.filter_by(
                        id=entry[4],
                    ).first()

                    response.append(
                        {
                            'book_series_id': str(book_series.id),
                            'author_first_name': entry[2],
                            'author_last_name': entry[3],
                            'book_name': entry[0].name,
                            'book_type': BookTypes.query.filter_by(id=entry[0].type_id).first().type_name,
                            'status': book_series.status,
                            'book_series': book_series.series,
                        }
                    )

                for i in book_author_join.iter_pages(left_edge=2, right_edge=2, left_current=2, right_current=2):
                    num_list.append(i)
            data = sorted(response, key=lambda e: e['status'], reverse=True)
            return jsonify(
                data=data.copy(),
                pages_lst=[value for value in num_list]
            )
        print(form.errors)
        return jsonify(data=form.errors)


@app.route("/admin_dashboard_advanced_search_book/", methods=["POST"])
@login_required
def admin_dashboard_advanced_search_book():
    response = []
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
                    book_series_status = "taken"
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
                        .join(BookSeries, BookSeries.book_id == Book.id) \
                        .filter(BookSeries.status == book_series_status) \
                        .order_by(Book.name) \
                        .add_columns(Author.id, Author.first_name, Author.last_name, BookSeries.id, BookSeries.series,
                                     BookSeries.status) \
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
                        .add_columns(Author.id, Author.first_name, Author.last_name, BookSeries.id, BookSeries.series,
                                     BookSeries.status) \
                        .paginate(
                        per_page=15,
                        page=form.page_number.data,
                        error_out=True
                    )

            if book_author_join:
                for entry in book_author_join.items:
                    response.append({
                        'book_series_id': entry[4],
                        'author_first_name': entry[2],
                        'author_last_name': entry[3],
                        'book_name': entry[0].name,
                        'book_type': BookTypes.query.filter_by(id=entry[0].type_id).first().type_name,
                        'status': entry[6],
                        'book_series': entry[5]
                    }
                    )
                for i in book_author_join.iter_pages(left_edge=2, right_edge=2, left_current=2, right_current=2):
                    num_list.append(i)

            data = sorted(response, key=lambda e: e['status'], reverse=True)
            return jsonify(
                data=data.copy(),
                pages_lst=[value for value in num_list]
            )
        return jsonify(data=form.errors)


@app.route("/update_book/", methods=["POST"])
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

        # just series
        if book_series.series != form.update_book_series.data:
            if book_series.status == "taken":
                return jsonify(
                    data={
                        'update_book_series': 'Can not be modified until the book is returned !'
                    }
                )
            book_series.series = form.update_book_series.data
            db.session.commit()
        # book name, author name, type
        if form.update_book_name.data != book_old.name \
                and (form.update_author_last_name.data != author_old.last_name
                     or form.update_author_first_name.data != author_old.first_name
        ) \
                and form.update_book_type != type_old.type_name:

            new_author = Author.query.filter_by(
                first_name=form.update_author_first_name.data,
                last_name=form.update_author_last_name.data
            ).first()
            if not new_author:
                new_author = Author(
                    first_name=form.update_author_first_name.data,
                    last_name=form.update_author_last_name.data,
                    created_at=datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
                        pytz.timezone('Europe/Bucharest'))
                )
                db.session.add(new_author)
                db.session.commit()
                db.session.refresh(new_author)

            type_new = BookTypes.query.filter_by(
                type_name=form.update_book_type.data
            ).first()
            if not type_new:
                type_new = BookTypes(
                    type_name=form.update_book_type.data,
                    created_at=datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
                        pytz.timezone('Europe/Bucharest'))
                )
                db.session.add(type_new)
                db.session.commit()
                db.session.refresh(type_new)

            book_new = Book.query.filter_by(
                name=form.update_book_name.data,
            ).first()
            if book_new:
                return jsonify(
                    data={
                        'update_book_name': 'Book name already exists !'
                    }
                )

            if not book_new:
                book_new = Book(
                    name=form.update_book_name.data,
                    count_total=1,
                    count_free_books=1,
                    type_id=type_new.id,
                    author_id=new_author.id,
                    created_at=datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
                        pytz.timezone('Europe/Bucharest'))
                )
                db.session.add(book_new)
                db.session.commit()
                db.session.refresh(book_new)

            all_book_series = BookSeries.query.filter_by(book_id=book_old.id).all()
            for entry in all_book_series:
                entry.book_id = book_new.id
                db.session.commit()

            db.session.delete(book_old)
            db.session.commit()

            count = Book.query.filter_by(author_id=author_old.id).count()
            if count == 0:
                db.session.delete(author_old)
                db.session.commit()
            count = Book.query.filter_by(type_id=type_old.id).count()
            if count == 0:
                db.session.delete(type_old)
                db.session.commit()

        # book name and author
        elif form.update_book_name.data != book_old.name \
                and (form.update_author_last_name.data != author_old.last_name
                     or form.update_author_first_name.data != author_old.first_name
        ):

            new_author = Author.query.filter_by(
                first_name=form.update_author_first_name.data,
                last_name=form.update_author_last_name.data
            ).first()
            if not new_author:
                new_author = Author(
                    first_name=form.update_author_first_name.data,
                    last_name=form.update_author_last_name.data,
                    created_at=datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
                        pytz.timezone('Europe/Bucharest'))
                )
                db.session.add(new_author)
                db.session.commit()
                db.session.refresh(new_author)

            book_new = Book.query.filter_by(
                name=form.update_book_name.data,
            ).first()
            if book_new:
                return jsonify(
                    data={
                        'update_book_name': 'Book name already exists !'
                    }
                )

            if not book_new:
                book_new = Book(
                    name=form.update_book_name.data,
                    count_total=1,
                    count_free_books=1,
                    type_id=type_old.id,
                    author_id=new_author.id,
                    created_at=datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
                        pytz.timezone('Europe/Bucharest'))
                )
                db.session.add(book_new)
                db.session.commit()
                db.session.refresh(book_new)

            all_book_series = BookSeries.query.filter_by(book_id=book_old.id).all()
            for entry in all_book_series:
                entry.book_id = book_new.id
                db.session.commit()

            db.session.delete(book_old)
            db.session.commit()

            count = Book.query.filter_by(author_id=author_old.id).count()
            if count == 0:
                db.session.delete(author_old)
                db.session.commit()

        # book name and type
        elif form.update_book_name.data != book_old.name and form.update_book_type.data != type_old.type_name:

            type_new = BookTypes.query.filter_by(
                type_name=form.update_book_type.data
            ).first()
            if not type_new:
                type_new = BookTypes(
                    type_name=form.update_book_type.data,
                    created_at=datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
                        pytz.timezone('Europe/Bucharest'))
                )
                db.session.add(type_new)
                db.session.commit()
                db.session.refresh(type_new)

            book_new = Book.query.filter_by(
                name=form.update_book_name.data,
            ).first()
            if book_new:
                return jsonify(
                    data={
                        'update_book_name': 'Book name already exists !'
                    }
                )

            if not book_new:
                book_new = Book(
                    name=form.update_book_name.data,
                    count_total=1,
                    count_free_books=1,
                    type_id=type_new.id,
                    author_id=author_old.id,
                    created_at=datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
                        pytz.timezone('Europe/Bucharest'))
                )
                db.session.add(book_new)
                db.session.commit()
                db.session.refresh(book_new)

            all_book_series = BookSeries.query.filter_by(book_id=book_old.id).all()
            for entry in all_book_series:
                entry.book_id = book_new.id
                db.session.commit()

            db.session.delete(book_old)
            db.session.commit()

            count = Book.query.filter_by(type_id=type_old.id).count()
            if count == 0:
                db.session.delete(type_old)
                db.session.commit()

        # type and author
        elif (
                form.update_author_last_name.data != author_old.last_name or form.update_author_first_name.data != author_old.first_name) \
                and (form.update_book_type.data != type_old.type_name):

            new_author = Author.query.filter_by(
                first_name=form.update_author_first_name.data,
                last_name=form.update_author_last_name.data
            ).first()
            if not new_author:
                new_author = Author(
                    first_name=form.update_author_first_name.data,
                    last_name=form.update_author_last_name.data,
                    created_at=datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
                        pytz.timezone('Europe/Bucharest'))
                )
                db.session.add(new_author)
                db.session.commit()
                db.session.refresh(new_author)

            type_new = BookTypes.query.filter_by(
                type_name=form.update_book_type.data
            ).first()
            if not type_new:
                type_new = BookTypes(
                    type_name=form.update_book_type.data,
                    created_at=datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
                        pytz.timezone('Europe/Bucharest'))
                )
                db.session.add(type_new)
                db.session.commit()
                db.session.refresh(type_new)

            book_old.author_id = new_author.id
            book_old.type_id = type_new.id

            db.session.commit()

            count = Book.query.filter_by(author_id=author_old.id).count()
            if count == 0:
                db.session.delete(author_old)
                db.session.commit()
            count = Book.query.filter_by(type_id=type_old.id).count()
            if count == 0:
                db.session.delete(type_old)
                db.session.commit()

        # just book name
        elif form.update_book_name.data != book_old.name:

            book_new = Book.query.filter_by(
                name=form.update_book_name.data,
            ).first()
            if book_new:
                return jsonify(
                    data={
                        'update_book_name': 'Book name already exists !'
                    }
                )

            if not book_new:
                book_new = Book(
                    name=form.update_book_name.data,
                    count_total=1,
                    count_free_books=1,
                    type_id=type_old.id,
                    author_id=author_old.id,
                    created_at=datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
                        pytz.timezone('Europe/Bucharest'))
                )
                db.session.add(book_new)
                db.session.commit()
                db.session.refresh(book_new)

            all_book_series = BookSeries.query.filter_by(book_id=book_old.id).all()
            for entry in all_book_series:
                entry.book_id = book_new.id
                db.session.commit()

            db.session.delete(book_old)
            db.session.commit()

        # just book type
        elif form.update_book_type.data != type_old.type_name:
            type_new = BookTypes.query.filter_by(
                type_name=form.update_book_type.data
            ).first()
            if not type_new:
                type_new = BookTypes(
                    type_name=form.update_book_type.data,
                    created_at=datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
                        pytz.timezone('Europe/Bucharest'))
                )
                db.session.add(type_new)
                db.session.commit()
                db.session.refresh(type_new)

            book_old.type_id = type_new.id
            db.session.commit()

            count = Book.query.filter_by(type_id=type_old.id).count()
            if count == 0:
                db.session.delete(type_old)
                db.session.commit()

        # just author name
        elif form.update_author_first_name.data != author_old.first_name \
                or form.update_author_last_name.data != author_old.last_name:

            new_author = Author.query.filter_by(
                first_name=form.update_author_first_name.data,
                last_name=form.update_author_last_name.data
            ).first()
            if not new_author:
                new_author = Author(
                    first_name=form.update_author_first_name.data,
                    last_name=form.update_author_last_name.data,
                    created_at=datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
                        pytz.timezone('Europe/Bucharest'))
                )
                db.session.add(new_author)
                db.session.commit()
                db.session.refresh(new_author)

            book_old.author_id = new_author.id
            db.session.commit()

            count = Book.query.filter_by(author_id=author_old.id).count()
            if count == 0:
                db.session.delete(author_old)
                db.session.commit()

        return jsonify(
            data={
                'id': str(form.update_book_series_id.data)
            }
        )
    else:
        print(form.errors)
        return jsonify(data=form.errors)


@app.route("/delete_book_series/<int:id>/", methods=["DELETE"])
@login_required
def delete_book_series(id):
    if current_user.type != "admin":
        return render_template("page_403.html")

    book_series = BookSeries.query.filter_by(id=id).first()
    if not book_series:
        return render_template("page_404.html")

    book = Book.query.filter_by(id=book_series.book_id).first()
    if not book:
        return render_template("page_404.html")

    count_series = book.count_total
    next_books = NextBook.query.filter_by(id_series_book=book_series.id).all()

    for next in next_books:
        next.id_book = 0
        next.id_series_book = 0
        next.rank = 0
        next.status = "None"
        next.period = 0
        db.session.commit()
    entry_logs = EntryLog.query.filter_by(id_book_series=book_series.id).all()

    for entry_log in entry_logs:
        db.session.delete(entry_log)
        db.session.commit()

    db.session.delete(book_series)
    db.session.commit()

    if count_series == 1:
        author = Author.query.filter_by(id=book.author_id).first()
        count_author_books = Book.query.filter_by(author_id=author.id).count()
        if count_author_books == 1:
            db.session.delete(author)

        entry_wishlist = EntryWishlist.query.filter_by(id_book=book.id).all()

        for entry in entry_wishlist:
            db.session.delete(entry)
            db.session.commit()

        count_type_books = Book.query.filter_by(type_id=book.type_id).count()
        if count_type_books == 1:
            BookTypes.query.filter_by(id=book.type_id).delete()
            db.session.commit()

        db.session.delete(book)
        db.session.commit()
    else:
        book.count_total -= 1
        book.count_free_books -= 1
        db.session.commit()

    return jsonify(
        data={
            'id': id
        }
    )


@app.route("/get_user_taken_book/<int:id>/", methods=["GET"])
@login_required
def get_user_taken_book(id):
    if current_user.type != "admin":
        return render_template("page_403.html")

    entry_log = db.session() \
        .query(EntryLog) \
        .filter(
        (EntryLog.id_book_series == id)
        & (EntryLog.status.in_(["Reserved", "Unreturned"]))
    ).first()
    if not entry_log:
        return not_found("nu exista cartea")

    log = Log.query.filter_by(id=entry_log.id_log).first()
    user = User.query.filter_by(id=log.id_user).first()
    return jsonify(
        data={
            'user_first_name': user.first_name,
            'user_last_name': user.last_name,
            'user_library_card_id': user.library_card_id,
            'user_trust_coeff': user.trust_coeff,
            'user_entry_status': entry_log.status,
            'user_period_start': entry_log.period_start,
            'user_period_end': entry_log.period_end,
            'user_period_diff': entry_log.period_diff
        }
    )


def get_diff_seconds(diff):
    days = '0'
    hours = '0'
    minutes = '0'
    seconds = '0'
    match_days = re.search("\s*(\d+)\s*days?", str(diff))
    if match_days:
        days = match_days.groups(0)[0]
    match = re.search("(\d+):(\d+):(\d+)", str(diff))
    if match:
        hours, minutes, seconds = match.groups()

    total = timedelta(days=int(days), hours=int(hours), minutes=int(minutes), seconds=int(seconds))
    return total.total_seconds()


@app.route("/rent_book/<int:id>/", methods=["GET"])
@login_required
def rent_book(id):
    if current_user.type != "admin":
        return render_template("page_403.html")

    entry_log = db.session() \
        .query(EntryLog) \
        .filter(
        (EntryLog.id_book_series == id)
        & (EntryLog.status.in_(["Reserved", "Unreturned"]))
    ).first()
    if not entry_log:
        return not_found("nu exista cartea")

    log = Log.query.filter_by(id=entry_log.id_log).first()
    user = User.query.filter_by(id=log.id_user).first()
    if entry_log.status == "Reserved":
        entry_log.status = "Unreturned"
        db.session.commit()
        return jsonify(
            data={
                'id': entry_log.id,
            }
        )
    else:

        diff = entry_log.period_end - entry_log.period_start
        period_max = get_diff_seconds(diff)

        time_now = datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(pytz.timezone('Europe/Bucharest'))
        period_current = get_diff_seconds(time_now - entry_log.period_start)
        procent = 0

        if period_max != 0:
            procent = (100 * period_current) / period_max
            procent = int(float("{0:.0f}".format(procent)))
            procent = 100 - procent

        user.trust_coeff += procent
        user.count_books_returned += 1
        db.session.commit()
        entry_log.status = "Returned"
        db.session.commit()

        book_series = BookSeries.query.filter_by(id=entry_log.id_book_series).first()
        book_series.status = "available"
        db.session.commit()

        book = Book.query.filter_by(id=book_series.book_id).first()
        book.count_free_books += 1
        db.session.commit()

        next_book = NextBook.query.filter_by(
            id_user=current_user.id,
            status="Have one"
        ).first()

        if next_book:
            next_book.rank = 0
            next_book.period = 0
            next_book.status = "None"
            db.session.commit()

        return jsonify(
            data={
                'procent': procent,
            }
        )
