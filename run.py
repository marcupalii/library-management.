
from app import app

if __name__ == '__main__':

    app.run(host='localhost')



# in ..\app\
# celery worker --app=app.celery --pool=eventlet --loglevel=INFO
# celery -A app.celery beat --loglevel=info