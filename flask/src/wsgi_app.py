import os
import sys

from gevent import monkey

monkey.patch_all()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

from app import app  # noqa
