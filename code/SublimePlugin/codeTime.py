import sublime_plugin
import sublime
from datetime import datetime as dt
import sys
from .periodicLogSaver import PeriodicLogSaver
import json
import mimetypes
import urllib
import platform
import os

# define local variables
file_times_dict = {}
periodic_log_save_timeout = 300  # seconds
periodic_log_save_on = True

user_id = ""

if platform.system() == 'Windows':
    DATA_FOLDER_PATH = os.path.join(os.getenv('APPDATA'), 'codeTime')
else:
    DATA_FOLDER_PATH = os.path.join(os.path.expanduser('~'), 'codeTime')

if not os.path.exists(DATA_FOLDER_PATH):
    os.makedirs(DATA_FOLDER_PATH)

try:
    f = open(DATA_FOLDER_PATH+"\\userid.txt", "r")
    user_id = f.readline()
    f.close()
except:
    print("Exception occured")
    f = open(DATA_FOLDER_PATH+"\\userid.txt", "w")
    response = (urllib.request.urlopen("http://152.46.17.237:8080/signup").read())
    user_id = (response.decode('utf-8'))
    f.write(user_id)
    f.close()


def when_activated(view):
    """
    Function to log start timestamp when a window is activated.

    Parameters
    ----------
    view: View class object
    """
    try:
        print(file_times_dict.keys())
        window = view.window()
        if window is not None:
            file_name = view.file_name()

            if file_name is not None:
                end_time = None
                start_time = dt.now().strftime('%Y-%m-%d %H:%M:%S')

                if(file_name in file_times_dict):
                    file_times_dict[file_name].append([start_time, end_time])
                else:
                    file_times_dict[file_name] = [[start_time, end_time]]

                print('File_name: ', file_name)
                print('\n ----- \n')
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print("codeTime:when_activated(): {error} on line number: {lno}".format(error=str(e), lno=str(exc_tb.tb_lineno)))  # noqa: E501


def when_deactivated(view):
    """
    Function to log end timestamp when a window is deactivated.

    Parameters
    ----------
    view: View class object
    """
    try:
        window = view.window()
        if window is not None:
            file_name = view.file_name()

            if file_name is not None:
                end_time = dt.now().strftime('%Y-%m-%d %H:%M:%S')
                file_times_dict[file_name][-1][1] = end_time

                print('File_name: ', file_name)
                print('\n ----- \n')
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print("codeTime:when_deactivated(): {error} on line number: {lno}".format(error=str(e), lno=str(exc_tb.tb_lineno)))  # noqa: E501


class CustomEventListener(sublime_plugin.EventListener):
    """
    Class which is a subclass of EventListener that has functions for save, window
    activate, window deactivate and window close events.
    """

    def on_activated(self, view):
        """
        Function which uses when_activated function to log data.

        Parameters
        ----------
        view: View class object
        """
        try:
            print(view.file_name(), 'is now the active view')
            when_activated(view)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print("codeTime:CustomEventListener():on_activated() {error} on line number: {lno}".format(error=str(e), lno=str(exc_tb.tb_lineno)))  # noqa: E501

    def on_deactivated(self, view):
        """
        Function which uses when_deactivated function to log data.

        Parameters
        ----------
        view: View class object
        """
        try:
            print(view.file_name(), 'is deactivated view')
            when_deactivated(view)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print("codeTime:CustomEventListener():on_deactivated() {error} on line number: {lno}".format(error=str(e), lno=str(exc_tb.tb_lineno)))  # noqa: E501

    def on_close(self, view):
        """
        Function which sends the data to the databse server when a window is closed.

        Parameters
        ----------
        view: View class object
        """
        try:
            print(view.file_name(), 'is no more')

            file_name = view.file_name()
            end_time = dt.now().strftime('%Y-%m-%d %H:%M:%S')
            print(file_times_dict)
            if file_name is not None and file_name in file_times_dict:
                if file_times_dict[file_name][-1][1] is None:
                    file_times_dict[file_name][-1][1] = end_time
                json_insert_data = {}
                json_insert_data["data"] = []
                file_type=(file_name.split('\\')[-1]).split('.')[-1]
                """
                file_type = mimetypes.guess_type(file_name)
                if file_type[0] is not None:
                    file_type = file_type[0].split("/")[-1].split("-")[-1]
                else:
                    file_type = "other"
                """
                for i in range(len(file_times_dict[file_name])):
                    json_insert_data["data"].append({'uid':user_id, "file_name": file_name,
                                                     "start_date": file_times_dict[file_name][i][0], "end_date": file_times_dict[file_name][i][1],  "file_type": file_type })

                data = json.dumps(json_insert_data).encode('utf-8')
                req = urllib.request.Request("http://152.46.17.237:8080/send", data=data,
                             headers={'content-type': 'application/json'})
                response = urllib.request.urlopen(req)
                print(response)
                file_times_dict.pop(file_name)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print("codeTime:CustomEventListener():on_close() {error} on line number: {lno}".format(error=str(e), lno=str(exc_tb.tb_lineno)))  # noqa: E501


def plugin_loaded():

    print("Plugin Loaded")
    try:
        if periodic_log_save_on:
            periodcLogSaver = PeriodicLogSaver(kwargs={'inMemoryLog': file_times_dict, 'timeout': periodic_log_save_timeout, 'user_id': user_id})  # noqa: E501
            periodcLogSaver.start()
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print("codeTime:plugin_loaded() {error} on line number: {lno}".format(error=str(e), lno=str(exc_tb.tb_lineno)))  # noqa: E501
