from flask import render_template, url_for, redirect, jsonify
from app import app, db
from flask_login import current_user, login_required
from app.forms import Add_user, Advanced_search_users, Basic_search_users, Update_user
import os
from app import APP_ROOT
from werkzeug.utils import secure_filename
from app.models import User, Wishlist, NextBook, User_settings, EntryWishlist, Log, EntryLog
import hashlib
from datetime import datetime, timedelta
import pytz
import re

ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/users")
@login_required
def users():
    new_user = Add_user()
    basic_search_form = Basic_search_users()
    advanced_search_form = Advanced_search_users()
    update_user = Update_user()
    return render_template(
        "users.html",
        new_user=new_user,
        update_user=update_user,
        basic_search_form=basic_search_form,
        advanced_search_form=advanced_search_form
    )


@app.route('/add_user/', methods=['GET', 'POST'])
@login_required
def add_user():
    form = Add_user()
    if form.validate_on_submit():
        target = re.sub("[\\\]+", "/", os.path.join(APP_ROOT, 'images'))
        filename = secure_filename(form.file.data.filename)
        if allowed_file(filename):
            destination = "/".join([target, filename])
            form.file.data.save(destination)

            exists_library_card_id = User.query.filter_by(
                library_card_id=form.library_card_id.data
            ).first()
            if exists_library_card_id:
                form.library_card_id.errors.append("Id already exists !")
                return render_template(
                    'users.html',
                    new_user=form
                )
            exists_email = User.query.filter_by(
                email=form.email.data
            ).first()
            if exists_email:
                form.email.errors.append("Email already exists !")
                return render_template(
                    'users.html',
                    new_user=form
                )

            user = User(
                library_card_id=form.library_card_id.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                address=form.address.data,
                city=form.city.data,
                country=form.city.data,
                zip_code=form.zip_code.data,
                email=form.email.data,
                password=hashlib.sha512(form.library_card_id.data.encode()).hexdigest(),
                type="user",
                trust_coeff=0,
                created_at=datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
                    pytz.timezone('Europe/Bucharest')),
            )
            db.session.add(user)
            db.session.commit()

            wishlist = Wishlist(
                user=user,
                created_at=datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
                    pytz.timezone('Europe/Bucharest'))
            )

            db.session.add(wishlist)
            db.session.commit()

            next_book = NextBook(
                user=user,
                period=0,
                status="None",
                created_at=datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
                    pytz.timezone('Europe/Bucharest')
                )
            )
            db.session.add(next_book)
            db.session.commit()

            settings = User_settings(
                user=user,
                created_at=datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(
                    pytz.timezone('Europe/Bucharest')
                )
            )
            db.session.add(settings)
            db.session.commit()

            db.session.refresh(user)
            new_name = re.sub("/[_a-zA-Z]+\.", "/" + str(user.id) + ".", destination)
            os.rename(destination, new_name)
            user.img_src = new_name.split(target)[1]
            db.session.commit()

            return redirect(url_for('users'))
        else:
            form.file.errors.append("Invalid extesion !")
            return render_template(
                'users.html',
                new_user=form
            )

    else:
        return render_template(
            'users.html',
            new_user=form
        )


@app.route("/admin_dashboard_basic_search_users/", methods=["POST"])
@login_required
def admin_dashboard_basic_search_users():
    response = {}
    num_list = []

    if current_user.email:
        form = Basic_search_users()
        if form.validate_on_submit():
            name = ""
            if form.basic_search_substring.data == False:
                name = form.basic_search_name.data if form.basic_search_name.data != "all" else "%%"
            else:
                name = '%' + form.basic_search_name.data + '%'

            users = User.query \
                .filter(
                (User.first_name.like(name) | User.last_name.like(name))
                    &(User.type == "user")
                ) \
                .paginate(
                per_page=15,
                page=form.basic_page_number.data,
                error_out=True
            )

            if users:
                for user in users.items:
                    response.update({
                        str(user.id): {
                            'user_first_name': user.first_name,
                            'user_last_name': user.last_name,
                            'user_type': user.type,
                            'user_email': user.email,
                            'user_trust_coeff': user.trust_coeff,
                            'user_library_card_id': user.library_card_id,
                            'user_address': user.address,
                            'user_city': user.city,
                            'user_country': user.country,
                            'user_zip_code': user.zip_code,
                        }
                    })

                for i in users.iter_pages(left_edge=2, right_edge=2, left_current=2, right_current=2):
                    num_list.append(i)
            print(response)
            return jsonify(
                data={key: response[key] for key in response.keys()},
                pages_lst=[value for value in num_list]
            )
        # print(form.errors)
        return jsonify(data=form.errors)


@app.route("/admin_dashboard_advanced_search_users/", methods=["POST"])
@login_required
def admin_dashboard_advanced_search_users():
    response = {}
    num_list = []

    if current_user.type == "admin":
        form = Advanced_search_users()
        # form.advanced_user_first_name.data
        # form.advanced_user_last_name.data
        # form.advanced_user_library_card_id.data
        # form.advanced_user_email.data
        if form.validate_on_submit():
            f_name = ""
            l_name = ""
            email = ""
            library_card_id = ""
            if form.search_substring.data == False:
                f_name = form.advanced_user_first_name.data if form.advanced_user_first_name.data else "%%"
                l_name = form.advanced_user_last_name.data if form.advanced_user_last_name.data else "%%"
                email = form.advanced_user_email.data if form.advanced_user_email.data else "%%"
                library_card_id = form.advanced_user_library_card_id.data if form.advanced_user_library_card_id.data else "%%"
            else:
                f_name = '%' + form.advanced_user_first_name.data + '%'
                l_name = '%' + form.advanced_user_last_name.data + '%'
                email = '%' + form.advanced_user_email.data + '%'
                library_card_id = '%' + form.advanced_user_library_card_id.data + '%'

            users = User.query \
                .filter(
                User.first_name.like(f_name)
                & User.last_name.like(l_name)
                & User.email.like(email)
                & User.library_card_id.like(library_card_id)
                & (User.type == "user")
            ) \
                .paginate(
                per_page=15,
                page=form.advanced_page_number.data,
                error_out=True
            )

            if users:
                for user in users.items:
                    response.update({
                        str(user.id): {
                            'user_first_name': user.first_name,
                            'user_last_name': user.last_name,
                            'user_type': user.type,
                            'user_email': user.email,
                            'user_trust_coeff': user.trust_coeff,
                            'user_library_card_id': user.library_card_id,
                            'user_address': user.address,
                            'user_city': user.city,
                            'user_country': user.country,
                            'user_zip_code': user.zip_code,
                        }
                    })

                for i in users.iter_pages(left_edge=2, right_edge=2, left_current=2, right_current=2):
                    num_list.append(i)
            print(response)
            return jsonify(
                data={key: response[key] for key in response.keys()},
                pages_lst=[value for value in num_list]
            )
        print(form.errors)
        return jsonify(data=form.errors)


@app.route("/update_user/", methods=["POST"])
@login_required
def update_user():
    if current_user.type != "admin":
        return render_template("page_403.html")

    form = Update_user()
    if form.validate_on_submit():
        user = User.query.filter_by(id=form.update_user_id.data).first()
        if not user:
            pass
        if user.type == "admin":
            return jsonify(
                data={
                    'update_user_type': 'Can not modify admin !'
                }
            )
        exists_email = User.query.filter_by(email=form.update_user_email.data).first()
        if exists_email and exists_email.id != form.update_user_id.data:
            return jsonify(
                data={
                    'update_user_email': 'Email already exists !'
                }
            )
        exists_library_card_id = User.query.filter_by(
            library_card_id=form.update_user_library_card_id.data
        ).first()
        if exists_library_card_id and exists_library_card_id.id != form.update_user_id.data:
            return jsonify(
                data={
                    'update_user_library_card_id': 'Library card id already exists !'
                }
            )
        user.first_name = form.update_user_first_name.data
        user.last_name = form.update_user_last_name.data
        user.email = form.update_user_email.data
        user.library_card_id = form.update_user_library_card_id.data
        user.city = form.update_user_city.data
        user.country = form.update_user_country.data
        user.zip_code = form.update_user_zip_code.data
        user.address = form.update_user_address.data
        db.session.commit()
        print(
            form.update_user_id.data,
            form.update_user_book_return_coeff.data,
            form.update_user_first_name.data,
            form.update_user_last_name.data,
            form.update_user_email.data,
            form.update_user_library_card_id.data,
            form.update_user_city.data,
            form.update_user_country.data,
            form.update_user_zip_code.data,
            form.update_user_address.data,
            form.update_user_type.data
        )
        return jsonify(
            data={
                'id': str(form.update_user_id.data)
            }
        )
    else:
        print(form.errors)
        return jsonify(data=form.errors)


@app.route("/delete_user/<int:id>/", methods=["DELETE"])
@login_required
def delete_user(id):
    if current_user.type != "admin":
        return render_template("page_403.html")

    user = User.query.filter_by(id=id).first()
    if user.type == "admin":
        return jsonify(
            data={
                'id': user.id
            }
        )
    next_book = user.next_book
    db.session.delete(next_book)
    # db.session.commit()

    wishlist = Wishlist.query.filter_by(id_user=user.id).first()
    entry_wishlists = EntryWishlist.query.filter_by(id_wishlist=wishlist.id).all()
    for entry in entry_wishlists:
        db.session.delete(entry)
        # db.session.commit()
    db.session.delete(wishlist)
    # db.session.commit()

    log = Log.query.filter_by(id_user=user.id).first()
    if log:
        entry_logs = EntryLog.query.filter_by(id_log=log.id).all()
        for entry in entry_logs:
            db.session.delete(entry)
            # db.session.commit()

        db.session.delete(log)

    id = user.id
    db.session.delete(user)
    db.session.commit()
    return jsonify(
        data={
            'id': id
        }
    )
