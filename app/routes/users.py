from flask import render_template, url_for, redirect
from app import app, db
from flask_login import current_user, login_required
from app.forms import Add_user
import os
from app import APP_ROOT
from werkzeug.utils import secure_filename
from app.models import User, Wishlist, NextBook, User_settings
import hashlib
from datetime import datetime, timedelta
import pytz
@app.route("/users")
@login_required
def users():
    new_user = Add_user()
    return render_template(
        "users.html",
        new_user=new_user
    )


import re


ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
            new_name = re.sub("/[_a-zA-Z]+\.","/"+str(user.id)+".",destination)
            os.rename(destination,new_name)
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
