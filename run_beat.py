import subprocess
import os
from pathlib import Path

MY_FILE = "celerybeat.pid"
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
PARTITION = str(ROOT_PATH.partition(os.path.sep)[0])
START_BEAT = "celery -A app.celery beat --loglevel=info"
if __name__ == "__main__":
    fp = Path(ROOT_PATH + "\\"+ MY_FILE)
    if fp.is_file():
        os.remove(ROOT_PATH + "\\"+ MY_FILE)
    command = ROOT_PATH + "\\venv\Scripts\\activate.bat & " + PARTITION + " & cd " + ROOT_PATH + " & " + START_BEAT
    p = subprocess.Popen(command, creationflags=subprocess.CREATE_NEW_CONSOLE)