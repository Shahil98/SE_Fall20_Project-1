import threading
import time
import copy
import sublime
from datetime import datetime as dt
import sys
import json
import urllib


class PeriodicLogSaver(threading.Thread):

    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, verbose=None):  # noqa: E128
        """
        Constructor for PeriodicLogSaver class.

        Parameters
        ----------
        kwargs: Dictionary containing dictionary of files and times, time period for log saver and user id
        """
        super(PeriodicLogSaver, self).__init__(
            group=group, target=target, name=name)
        self.args = args
        self.kwargs = kwargs
        return

    def run(self):
        while True:
            try:
                curr_file = sublime.active_window().active_view().file_name()

                if curr_file is not None:
                    inMemoryLogDeepCopy = copy.deepcopy(
                        self.kwargs['inMemoryLog'])
                    inMemoryLog = self.kwargs['inMemoryLog']
                    inMemoryLog.clear()

                    if curr_file in inMemoryLogDeepCopy:  # noqa: E501
                        end_time = dt.now().strftime('%Y-%m-%d %H:%M:%S')
                        inMemoryLogDeepCopy[curr_file][-1][1] = end_time

                        if curr_file not in inMemoryLog:
                            inMemoryLog[curr_file] = [[end_time, None]]

                        self.write_log_file(inMemoryLogDeepCopy)
                time.sleep(self.kwargs['timeout'])
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                print("periodicLogSaver:PeriodicLogSaver:run(): {error} on line number: {lno}".format(error=str(e), lno=str(exc_tb.tb_lineno)))  # noqa: E501

    def write_log_file(self, file_times_dict):
        """
        Function to send data to server

        Parameters
        ----------
        file_times_dict: dictionary with files and corresponding time information
        """
        try:
            json_insert_data = []
            for file_name in file_times_dict.keys():
                file_type = "."+(file_name.split('\\')[-1]).split('.')[-1]
                for i in range(len(file_times_dict[file_name])):
                    if(file_times_dict[file_name][i][1] == None):
                        file_times_dict[file_name][i][1] = dt.now().strftime('%Y-%m-%d %H:%M:%S')
                    json_insert_data.append({'uid': self.kwargs["user_id"], "file_name": file_name, "start_date": file_times_dict[file_name][i][0], "end_date": file_times_dict[file_name][i][1], "file_type": file_type})
            data = json.dumps(json_insert_data).encode('utf-8')
            req = urllib.request.Request(
                "http://152.46.17.237:8080/send", data=data, headers={'content-type': 'application/json'})
            response = urllib.request.urlopen(req)
            return response.getcode()

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print("periodicLogSaver:PeriodicLogSaver():write_log_file(): {error} on line number: {lno}".format(error=str(e), lno=str(exc_tb.tb_lineno)))  # noqa: E501
