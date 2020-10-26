import sublime
import sys
import io
from datetime import datetime as dt
from unittest import TestCase
from unittest.mock import Mock, patch
from code.SublimePlugin import codeTime

version = sublime.version()
# modules = sys.modules.keys()
# capturedOutput = io.StringIO()
# sys.stdout = capturedOutput
# print("\n$$$$$$\n", modules, "\n$$$$$$$$\n")
# sys.stdout = sys.__stdout__
# print('Captured', capturedOutput.getvalue())
# codeTime = sys.modules["SE_Fall20_Project-1.code.SublimePlugin.codeTime"]


class TestFunctions(TestCase):

    @patch('time.time', return_value=100)
    def test_when_activated(self, mock_time):
        view = Mock()
        view.filename.return_value = "sample.txt"
        # datetime = Mock()
        codeTime.when_activated(view)
        view.window.assert_called_once()

    def test_when_deactivated(self):
        view = Mock()
        view.file_name.return_value = "sample.txt"
        curr_date = dt.now().strftime('%Y-%m-%d')
        codeTime.file_times_dict[curr_date] = {'sample.txt': ["1234", None]}
        view.assert_called_once()
