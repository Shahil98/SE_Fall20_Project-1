import sublime
import sys
import os
# import io
from unittest import TestCase
from datetime import datetime as dt
from code.SublimePlugin import periodicLogSaver
# from unittest.mock import Mock, patch

version = sublime.version()
# modules = sys.modules.keys()
# capturedOutput = io.StringIO()
# sys.stdout = capturedOutput
# print("\n$$$$$$\n", modules, "\n$$$$$$$$\n")
# sys.stdout = sys.__stdout__
# print('Captured', capturedOutput.getvalue())
periodicLogSaver1 = sys.modules["SE_Fall20_Project-1.code.SublimePlugin.periodicLogSaver"]


class TestPeriodicLogSaver(TestCase):

    def test_write_log_file(self):
        file_times_dict = {'test_file.py': []}
        start_time = dt.now().strftime('%Y-%m-%d %H:%M:%S')
        end_time = dt.now().strftime('%Y-%m-%d %H:%M:%S')
        file_times_dict['test_file.py'].append([start_time, end_time])
        code = periodicLogSaver1.write_log_file(self, file_times_dict)
        assert code == 200
