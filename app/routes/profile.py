from flask import render_template, url_for, redirect, jsonify, send_file
from app import app, db
from flask_login import current_user, login_required
from app.forms import Wishlist_settings, Change_password, Profile
import hashlib
from app.models import User
from app import APP_ROOT
import re
import os
@app.route('/profile')
@login_required
def profile():
    wishlist_settings = Wishlist_settings()
    wishlist_settings.setting_option.default = str(current_user.settings.wishlist_option)
    wishlist_settings.process()

    change_password = Change_password()

    profile_form = Profile()
    profile_form.library_card_id.default = current_user.library_card_id
    profile_form.first_name.default = current_user.first_name
    profile_form.last_name.default = current_user.last_name
    profile_form.address.default = current_user.address
    profile_form.city.default = current_user.city
    profile_form.country.default = current_user.country
    profile_form.zip_code.default = current_user.zip_code
    profile_form.email.default = current_user.email
    profile_form.process()

    return render_template(
        "profile.html",
        wishlist_settings=wishlist_settings,
        change_password=change_password,
        profile_form=profile_form,
    )


@app.route("/get_profile_img",methods=["GET"])
@login_required
def get_profile_img():
    target = re.sub("[\\\]+", "/", os.path.join(APP_ROOT, 'images'))
    if current_user.img_src:
        return send_file(target+current_user.img_src, mimetype='image/gif')
    else:
        return send_file(target+"/default.png", mimetype='image/gif')

@app.route("/change_password/",methods=["POST"])
@login_required
def change_password():

    form = Change_password()

    if form.validate_on_submit():
        if current_user.password == hashlib.sha512(form.old_password.data.encode()).hexdigest():
            user = current_user
            user.password = hashlib.sha512(form.new_password.data.encode()).hexdigest()
            db.session.add(user)
            db.session.commit()

            return jsonify(data={
                'succes': '200'
            })
        else:
            return jsonify(data={
                'old_password': 'Incorrect password'
            })
    else:
        return jsonify(data=form.errors)