from app import app
import os
if __name__ == '__main__':
       app.run(host='localhost', threaded=True)


#   F:\RepoLibManagement\venv\Scripts\activate.bat & F: & cd F:\RepoLibManagement & celery worker --app=app.celery --pool=eventlet --loglevel=INFO
#   F:\RepoLibManagement\venv\Scripts\activate.bat & F: & cd F:\RepoLibManagement & celery -A app.celery beat --loglevel=info