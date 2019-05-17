from flask import render_template, url_for, redirect
from app import app
from flask_login import current_user, login_required
from app.forms import Wishlist_settings

@app.route('/profile')
@login_required
def profile():
    wishlist_settings = Wishlist_settings()
    wishlist_settings.setting_option.default = str(current_user.settings.wishlist_option)
    wishlist_settings.process()

    return render_template(
        "profile.html",
        wishlist_settings=wishlist_settings

    )
