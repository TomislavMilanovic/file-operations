import os

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = True
ALLOWED_HOSTS = ['localhost']

CSRF_COOKIE_SECURE = False

BASE_FILE_OPERATIONS_FOLDER = os.path.join(BASE_DIR, 'testfolder')
