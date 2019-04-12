import os
basedir = os.path.abspath(os.path.dirname(__file__))

POSTGRES = {
    'user': 'admin',
    'pw': 'admin',
    'db': 'library',
    'host': 'localhost',
    'port': '5432',
}

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CELERY_TIMEZONE = 'Europe/Bucharest'
    ENABLE_UTC = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
    CELERY_BROKER_URL = 'amqp://localhost//',
    CELERY_RESULT_BACKEND = 'db+postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
