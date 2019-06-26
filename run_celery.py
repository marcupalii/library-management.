import subprocess
import os
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
PARTITION = str(ROOT_PATH.partition(os.path.sep)[0])
START_CELERY = "celery worker --app=app.celery --pool=eventlet --loglevel=INFO"
if __name__ == "__main__":

    command = ROOT_PATH + "\\venv\Scripts\\activate.bat & " + PARTITION + " & cd " + ROOT_PATH + " & " + START_CELERY
    p = subprocess.Popen(command, creationflags=subprocess.CREATE_NEW_CONSOLE)