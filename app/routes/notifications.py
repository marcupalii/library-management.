from flask import render_template, url_for
from app import app
from app.models import User, Notifications
from flask_login import login_required, current_user
from app.forms import Wishlist_settings
import re

@app.route("/notifications/page/<page>/focus=<id>/")
@login_required
def notifications(page, id):
    next_url = url_for('notifications', page=1, id=0)
    prev_url = url_for('notifications', page=1, id=0)
    num_list = []
    response = []
    nr_of_pages = 1
    notifications = Notifications.query \
        .filter_by(id_user=current_user.id) \
        .order_by(Notifications.created_at.desc()) \
        .paginate(per_page=15,
                  page=int(page),
                  error_out=True
                  )
    per_page = 15
    index = 1
    if int(page) > 1:
        index = (int(page) - 1) * per_page + 1

    if notifications:
        for entry in notifications.items:
            response.append([
                index,
                entry.content,
                entry.status,
                re.search("(\d+-\d+-\d+\s+\d+:\d+:\d+)",str(entry.created_at)).groups(0)[0],
                entry.id,
            ])
            index += 1

        next_url = url_for('notifications', page=notifications.next_num, id=id) \
            if notifications.has_next else url_for('notifications', page=page, id=0)
        prev_url = url_for('notifications', page=notifications.prev_num, id=id) \
            if notifications.has_prev else url_for('notifications', page=page, id=0)

        for i in notifications.iter_pages(left_edge=2, right_edge=2, left_current=2, right_current=2):
            num_list.append(i)

        if len(num_list) != 0:
            nr_of_pages = num_list[-1]

    wishlist_settings = Wishlist_settings()
    wishlist_settings.setting_option.default = str(current_user.settings.wishlist_option)
    wishlist_settings.process()

    return render_template(
        "notifications.html",
        notifications=response,
        id_user=current_user.id,
        next_url=next_url,
        prev_url=prev_url,
        num_list=num_list,
        nr_of_pages=nr_of_pages,
        wishlist_settings=wishlist_settings
    )
