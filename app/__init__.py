
# print('importing init... %s' % __name__)
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import threading
import time
from app.schedule_module import schedule_stable_match


def create_app():
    new_app = Flask(__name__, instance_relative_config=True)
    new_app.config.from_object('config')
    new_db = SQLAlchemy(new_app)
    threading.Thread(target=schedule_stable_match, args=(time.time(),)).start()
    return (new_app, new_db)


app, db = create_app()
# cand execut models ca main module comm importul de mai jos,import circular
from app import routes



