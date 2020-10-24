import sys
import os

from .code.SublimePlugin.codeTime import *  # noqa: F401, F403

BASE_PATH = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(1, BASE_PATH)
