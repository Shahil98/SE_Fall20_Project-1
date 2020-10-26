import threading
import time
import copy
import sublime
import json
import urllib.request
from datetime import datetime as dt
import sys


class PeriodicLogSaver(threading.Thread):
    def __init__(
            self,
            group=None,
            target=None,
            name=None,
            args=(),
            kwargs=None,
            verbose=None,
    ):
        super(PeriodicLogSaver, self).__init__(
            group=group, target=target, name=name
        )
        self.args = args
        self.kwargs = kwargs
        return

    def run(self):
        while True:
            try:
                curr_file = sublime.active_window().active_view().file_name()
                curr_date = dt.now().strftime("%Y-%m-%d")

                if curr_file is not None:
                    inMemLog = self.kwargs["inMemoryLog"]
                    inMemoryLogDeepCopy = copy.deepcopy(inMemLog)
                    inMemoryLog = inMemLog
                    inMemoryLog.clear()

                    # Writing the current date and file inMemoryLogDeepCopy by calling write_log_file

                    if (
                            curr_date in inMemoryLogDeepCopy
                            and curr_file in inMemoryLogDeepCopy[curr_date]
                    ):
                        end_time = time.time()
                        cd = curr_date
                        cf = curr_file
                        inMemoryLogDeepCopy[cd][cf][-1][1] = end_time

                        if curr_date not in inMemoryLog:
                            inMemoryLog[curr_date] = {}

                        if curr_file not in inMemoryLog[curr_date]:
                            temp = [[end_time, None]]
                            inMemoryLog[curr_date][curr_file] = temp

                        self.write_log_file(inMemoryLogDeepCopy)
                time.sleep(self.kwargs["timeout"])
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                print(
                    "periodicLogSaver:PeriodicLogSaver:run(): {error} on line \
                        number: {lno}".format(
                        error=str(e), lno=str(exc_tb.tb_lineno)
                    )
                )

    def write_log_file(self, file_times_dict):
        try:

            obj = []
            api_token = self.kwargs["API_TOKEN"]
            file_type = (
                sublime.active_window().active_view().settings().get("syntax")
            )
            with open(self.kwargs["LOG_FILE_PATH"], "a") as f:

                for key, val in file_times_dict.items():
                    curr_date = key
                    file_dict = val

                    for file_name, times_list in file_dict.items():
                        for time_start_end in times_list:
                            f.write(
                                curr_date
                                + ","
                                + file_name
                                + ","
                                + str(time_start_end[0])
                                + ","
                                + str(time_start_end[1])
                                + "\n"
                            )  # noqa: E501
                            row = {}
                            row["file_name"] = file_name.split("/")[-1]
                            row["file_extension"] = file_name.split(".")[-1]
                            row["detected_language"] = file_type.split("/")[
                                -1
                            ].split(".")[-2]
                            row["log_date"] = curr_date
                            row["log_timestamp"] = str(time_start_end[0])
                            row["api_token"] = api_token
                            obj.append(row)

                req = urllib.request.Request(self.kwargs["REQUEST_URL"])
                req.add_header(
                    "Content-Type", "application/json; charset=utf-8"
                )
                jsondata = json.dumps(obj)
                jsondataasbytes = jsondata.encode("utf-8")
                req.add_header("Content-Length", len(jsondataasbytes))
                response = (urllib.request.urlopen(req, jsondataasbytes).read().decode()) # noqa F841

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(
                "periodicLogSaver:PeriodicLogSaver():write_log_file(): {error} \
                on line number: {lno}".format(
                    error=str(e), lno=str(exc_tb.tb_lineno)
                )
            )  # noqa: E501
