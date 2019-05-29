from flask import render_template, url_for, redirect, jsonify
from app import app, db
from flask_login import current_user, login_required
from app.forms import New_Book, Choose_Author
import hashlib
from app.models import User, Author


@app.route('/books')
@login_required
def books():
    if current_user.type != "admin":
        return render_template("page_403.html")
    new_book = New_Book()
    new_book.type_author.default = '1'
    new_book.process()
    choose_author = Choose_Author()
    return render_template(
        "books.html",
        new_book=new_book,
        choose_author=choose_author
    )


@app.route('/add_new_book/',methods=["POST"])
@login_required
def add_new_book():
    if current_user.type != "admin":
        return render_template("page_403.html")
    new_book = New_Book()

    if new_book.validate_on_submit():
        print(
            new_book.name.data,
            new_book.type.data,
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

@app.route("/choose_author/",methods=["POST"])
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

        authors= Author.query \
            .filter(Author.name.like(name)) \
            .order_by(Author.name) \
            .paginate(
            per_page=3,
            page=form.page_nr.data,
            error_out=True
        )

        if authors:
            for entry in authors.items:
                response.update({
                    str(entry.id): {
                        'name': entry.name,
                    }
                })
            for i in authors.iter_pages(left_edge=2, right_edge=2, left_current=2, right_current=2):
                num_list.append(i)

        return jsonify(
            data={key: response[key] for key in response.keys()},
            pages_lst=[value for value in num_list]
        )
    return jsonify(data=form.errors)