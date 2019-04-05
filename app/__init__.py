
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import threading
from app.schedule_module import schedule_routine
from config import DevelopmentConfig
from flask_bootstrap import Bootstrap
from flask_login import LoginManager

def create_app():
    new_app = Flask(__name__, instance_relative_config=True)
    new_app.config.from_object(DevelopmentConfig)
    new_db = SQLAlchemy(new_app)
    new_bootstrap = Bootstrap(new_app)
    new_routine_thread = threading.Thread(target=schedule_routine)

    new_login_manager = LoginManager()
    new_login_manager.init_app(new_app)
    new_login_manager.login_view = 'login'



    return new_app, new_db, new_routine_thread, new_bootstrap, new_login_manager


app, db, routine_thread, boostrap, login_manager = create_app()
# cand execut models importul trebuie comm
from app import routes



