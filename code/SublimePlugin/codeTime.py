import sublime_plugin
import sublime
import time
import platform
import os
from datetime import datetime as dt
import sys
import subprocess

from .periodicLogSaver import PeriodicLogSaver

# create data folder based on OS
if platform.system() == "Windows":
    DATA_FOLDER_PATH = os.path.join(os.getenv("APPDATA"), ".codeTime")
else:
    DATA_FOLDER_PATH = os.path.join(os.path.expanduser("~"), ".codeTime")

if not os.path.exists(DATA_FOLDER_PATH):
    os.makedirs(DATA_FOLDER_PATH)

# define log file path
LOG_FILE_PATH = os.path.join(DATA_FOLDER_PATH, ".sublime_logs")

# define local variables
file_times_dict = {}
periodic_log_save_timeout = 300  # seconds
periodic_log_save_on = True
api_token = ""
configs = None


def when_activated(view):
    try:
        window = view.window()
        if window is not None:
            file_name = view.file_name()

            if file_name is not None:
                start_time = time.time()
                end_time = None

                curr_date = dt.now().strftime("%Y-%m-%d")

                if curr_date not in file_times_dict:
                    file_times_dict[curr_date] = {}

                if file_name not in file_times_dict[curr_date]:

                    file_times_dict[curr_date][file_name] = [
                        [start_time, end_time]
                    ]  # noqa: E501
                else:
                    file_times_dict[curr_date][file_name].append(
                        [start_time, end_time]
                    )  # noqa: E501

                print("File_name: ", file_name)
                print("\n ----- \n")
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(
            "codeTime:when_activated(): {error} on line number: {lno}".format(
                error=str(e), lno=str(exc_tb.tb_lineno)
            )
        )  # noqa: E501


def when_deactivated(view):
    try:
        window = view.window()
        if window is not None:
            file_name = view.file_name()

            if file_name is not None:
                end_time = time.time()

                curr_date = dt.now().strftime("%Y-%m-%d")

                file_times_dict[curr_date][file_name][-1][1] = end_time

                print("File_name: ", file_name)
                print("\n ----- \n")
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(
            "codeTime:when_deactivated(): {error} on line number: {lno}".format(
                error=str(e), lno=str(exc_tb.tb_lineno)
            )
        )  # noqa: E501


class CustomEventListener(sublime_plugin.EventListener):
    def on_post_save(self, view):
        print(view.file_name(), "just got saved")

    def on_activated(self, view):
        try:
            print(view.file_name(), "is now the active view")
            when_activated(view)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(
                "codeTime:CustomEventListener():on_activated() {error} on line number: {lno}".format(
                    error=str(e), lno=str(exc_tb.tb_lineno)
                )
            )  # noqa: E501

    def on_deactivated(self, view):
        try:
            print(view.file_name(), "is deactivated view")
            when_deactivated(view)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(
                "codeTime:CustomEventListener():on_deactivated() {error} on line number: {lno}".format(
                    error=str(e), lno=str(exc_tb.tb_lineno)
                )
            )  # noqa: E501

    def on_close(self, view):
        try:
            print(view.file_name(), "is no more")

            file_name = view.file_name()
            curr_date = dt.now().strftime("%Y-%m-%d")
            if (
                    file_name is not None
                    and file_name in file_times_dict[curr_date]
            ):

                end_time = time.time()

                last_time_list = file_times_dict[curr_date][file_name][-1]

                if last_time_list[1] is None:
                    last_time_list[1] = end_time

                with open(LOG_FILE_PATH, "a") as f:
                    for _time in file_times_dict[curr_date][file_name]:
                        f.write(
                            curr_date
                            + ","
                            + file_name
                            + ","
                            + str(_time[0])
                            + ","
                            + str(_time[1])
                            + "\n"
                        )  # noqa: E501
                file_times_dict[curr_date].pop(file_name, None)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(
                "codeTime:CustomEventListener():on_close() {error} on line number: {lno}".format(
                    error=str(e), lno=str(exc_tb.tb_lineno)
                )
            )  # noqa: E501


# view.run_command('dashboard')
class DashboardCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # Load config file
        configs = sublime.load_settings("CustomPreferences.sublime-settings")
        try:
            print("Showing Graphs")
            dir_path = os.path.dirname(os.path.realpath(__file__))
            subprocess.Popen(
                configs.get("python-env") + "'" + dir_path + "/output.py'",
                shell=True,
                stdout=subprocess.PIPE,
            )  # noqa: E501, F841
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print("codeTime:DashboardCommand():run() {error} on line number: {lno}".format(error=str(e), lno=str(exc_tb.tb_lineno)))


def plugin_loaded():
    try:
        configs = sublime.load_settings("CustomPreferences.sublime-settings")
        periodic_log_save_timeout = configs.get("timeout")
        api_token = configs.get("api_token")
        request_url = configs.get("request-url")
        if periodic_log_save_on:
            periodcLogSaver = PeriodicLogSaver(
                kwargs={
                    "inMemoryLog": file_times_dict,
                    "timeout": periodic_log_save_timeout,
                    "LOG_FILE_PATH": LOG_FILE_PATH,
                    "API_TOKEN": api_token,
                    "REQUEST_URL": request_url,
                }
            )  # noqa: E501
            periodcLogSaver.start()
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(
            "codeTime:plugin_loaded() {error} on line number: {lno}".format(
                error=str(e), lno=str(exc_tb.tb_lineno)
            )
        )  # noqa: E501
