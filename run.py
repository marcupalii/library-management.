
from app import app

if __name__ == '__main__':

    app.run(host='localhost')

# in ..\app\

# C:\Users\marcu\Desktop\Repository\env\Scripts\activate.bat
# cd C:\Users\marcu\Desktop\Repository
# celery worker --app=app.celery --pool=eventlet --loglevel=INFO
# celery -A app.celery beat --loglevel=info