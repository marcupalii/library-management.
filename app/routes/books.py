from flask import render_template, url_for, redirect, jsonify
from app import app, db
from flask_login import current_user, login_required
from app.forms import New_Book, Choose_Author, New_author, Basic_search, Advanced_search_admnin
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
    new_author = New_author()
    basic_search_form = Basic_search()
    advanced_search_form = Advanced_search_admnin()
    return render_template(
        "books.html",
        new_book=new_book,
        choose_author=choose_author,
        new_author=new_author,
        basic_search_form=basic_search_form,
        advanced_search_form=advanced_search_form,
    )


@app.route('/add_new_book/', methods=["POST"])
@login_required
def add_new_book():
    if current_user.type != "admin":
        return render_template("page_403.html")
    new_book = New_Book()

    if new_book.validate_on_submit():
        print(
            new_book.name.data,
            new_book.type.data,
            new_book.type_string_field.data,
            new_book.series.data,
            new_book.author_first_name.data,
            new_book.author_last_name.data
        )
        return jsonify(data={
            'id': 3,
            'code': 200
        })
    else:
        print(new_book.errors)
        return jsonify(data=new_book.errors)


@app.route("/add_new_author/", methods=["POST"])
@login_required
def add_new_author():
    new_author = New_author()
    if new_author.validate_on_submit():
        print(new_author.new_author_first_name.data, new_author.new_author_last_name.data)
        author = Author.query.filter_by(
            first_name=new_author.new_author_first_name.data,
            last_name=new_author.new_author_last_name.data
        ).first()

        if not author:
            author = Author(
                first_name=new_author.new_author_first_name.data,
                last_name=new_author.new_author_last_name.data,
                created_at=datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
                    pytz.timezone('Europe/Bucharest'))
            )
            db.session.add(author)
            db.session.commit()
            return jsonify(data={
                'status': 200
            })
        else:
            return jsonify(
                data={
                    'new_author_first_name': 'Author already exists !',
                    'new_author_last_name': 'Author already exists !',
                }
            )
    else:
        print(new_author.errors)
        return jsonify(data=new_author.errors)


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
            print(response)
            return jsonify(
                data={key: response[key] for key in response.keys()},
                pages_lst=[value for value in num_list]
            )
        print(form.errors)
        return jsonify(data=form.errors)
