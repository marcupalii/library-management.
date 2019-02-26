# print('importing run... %s' % __name__)
from app import app, routine_thread

if __name__ == '__main__':
    routine_thread.start()
    app.run()


# export FLASK_APP=app.py
# flask run