
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import threading
from app.schedule_module import schedule_routine
from config import DevelopmentConfig

def create_app():
    new_app = Flask(__name__, instance_relative_config=True)
    new_app.config.from_object(DevelopmentConfig)
    new_db = SQLAlchemy(new_app)
    new_routine_thread = threading.Thread(target=schedule_routine)
    return new_app, new_db, new_routine_thread


app, db, routine_thread = create_app()
# cand execut models importul trebuie comm
from app import routes



