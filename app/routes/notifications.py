from flask import render_template
from app import app
from app.models import User, Notifications
from flask_login import login_required, current_user


@app.route("/notifications")
@login_required
def notifications():
    _email = current_user.email
    response = []
    if _email:
        _user = User.query.filter_by(email=_email).first()

        _notifications = Notifications.query.filter_by(id_user=_user.id).order_by(Notifications.created_at.desc()).all()

        if _notifications:
            for notification in _notifications:
                response.append([
                    notification.id,
                    notification.content,
                    notification.status,
                    notification.created_at
                ])

        return render_template("notifications.html", notifications=response, id_user=current_user.id)
