# print('importing run... %s' % __name__)
from app import app

if __name__ == '__main__':

    app.run(host='localhost')


# export FLASK_APP=app.py
# flask run