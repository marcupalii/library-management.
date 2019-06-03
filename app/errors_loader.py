from flask import render_template, request, url_for, redirect, abort, jsonify, make_response, session
from app import app, login_manager, db
from app.models import User



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.errorhandler(401)
def FUN_401(error):
    return render_template("page_401.html"), 401


@app.errorhandler(403)
def FUN_403(error):
    return render_template("page_403.html"), 403


@app.errorhandler(404)
def not_found(error):
    """
    Gives error message when any invalid url are requested.
    Args:
        error (string):
    Returns:
        Error message.
    """
    print(error)
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(405)
def FUN_405(error):
    return render_template("page_405.html"), 405

