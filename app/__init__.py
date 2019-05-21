
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import DevelopmentConfig
from flask_login import LoginManager
from celery import Celery
import celeryconfig
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)
    celery.config_from_object(celeryconfig)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask

    return celery

def create_app():
    new_app = Flask(__name__)
    new_app.config.from_object(DevelopmentConfig)
    new_celery = make_celery(new_app)
    new_db = SQLAlchemy(new_app)

    new_login_manager = LoginManager()
    new_login_manager.init_app(new_app)
    new_login_manager.login_view = 'login'

    return new_app, new_db, new_celery, new_login_manager


app, db, celery, login_manager = create_app()

from app import errors_loader
from app.routes.login import login, process_login_form, logout
from app.routes.about import about
from app.routes.account import account, add_to_reserved, add_to_wishlist, mark_notification_read, Advanced_search, Basic_search, get_notification,save_settings, books_count
from app.routes.books_log import books_log, reserved_book
from app.routes.notifications import notifications
from app.routes.wishlist import wishlist_delete_entry, wishlist, wishlist_book, accept_next_book
from app.routes.profile import profile,change_password
from app.routes.admin import admin


