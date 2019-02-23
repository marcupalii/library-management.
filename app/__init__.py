

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

next_book = dict()
app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
db = SQLAlchemy(app)

# cand execut models ca main module comm importul de mai jos,import circular
from app import routes



