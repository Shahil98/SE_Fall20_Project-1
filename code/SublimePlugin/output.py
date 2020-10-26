#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 20 23:41:40 2020

@author: nirav
"""
import mimetypes
from plotly.offline import plot
from plotly import graph_objs as go
from collections import defaultdict
from datetime import datetime
from plotly import tools
import platform
import os


def show_graphs():
    if platform.system() == "Windows":
        DATA_FOLDER_PATH = os.path.join(os.getenv("APPDATA"), ".codeTime")
    else:
        DATA_FOLDER_PATH = os.path.join(os.path.expanduser("~"), ".codeTime")
    LOG_FILE_PATH = os.path.join(DATA_FOLDER_PATH, ".sublime_logs")

    sample_data = open(LOG_FILE_PATH, "r").read()
    logs = sample_data.split("\n")

    logs_dict = {}
    for log in logs[:-1]:
        try:
            log_date, log_file_path, start_time, end_time = log.split(",")

            end_time, start_time = float(end_time), float(start_time)
            file_type = mimetypes.guess_type(log_file_path)

            if file_type[0] is not None:
                file_type = file_type[0].split("/")[-1].split("-")[-1]
            else:
                file_type = "other"

            logs_dict[log_file_path] = {
                "st": start_time,
                "dt": datetime.strptime(log_date, "%Y-%m-%d"),
                "et": end_time,
                "duration": end_time - start_time,
                "type": file_type,
            }  # noqa: E501
        except Exception:
            continue

    fig = tools.make_subplots(
        rows=3,
        cols=2,
        shared_xaxes=True,
        specs=[
            [{"colspan": 2}, None],  # noqa: E501
            [{"type": "pie"}, {"type": "pie"}],  # noqa: E128
            [{"colspan": 2, "type": "table"}, None],
        ],
    )

    # ###############################- Pie Chart-
    durations = defaultdict(int)
    for file_path in logs_dict.keys():
        duration = logs_dict[file_path]["duration"]
        file_type = logs_dict[file_path]["type"]
        durations[file_type] += duration

    trace_timespan = go.Pie(
        labels=list(durations.keys()), values=list(durations.values())
    )  # noqa: E501

    fig.append_trace(trace_timespan, 2, 1)
    fig.append_trace(trace_timespan, 2, 2)
    # ##############################

    # ##############################-Time fill graph per filetype

    durations = defaultdict(dict)
    for file_path in logs_dict.keys():
        duration = logs_dict[file_path]["duration"]
        file_type = logs_dict[file_path]["type"]
        date = logs_dict[file_path]["dt"]

        if date in durations[file_type]:
            durations[file_type][date] += duration
        else:
            durations[file_type][date] = duration

    data = []
    for file_type in durations.keys():
        trace_timespan = go.Scatter(
            x=list(durations[file_type].keys()),
            y=list(durations[file_type].values()),
            name=file_type,
            fill="tozeroy",
        )  # noqa: E501

        # data.append(trace_timespan)
        fig.append_trace(trace_timespan, 1, 1)
    # fig = go.Figure(data=data)
    # plot(fig,filename="weekly_duration.html")
    # ##############################

    # ##############################-Time fill graph per filetype
    file_wise_durations = defaultdict(int)
    for filepath in logs_dict.keys():
        file_wise_durations[filepath] += logs_dict[filepath]["duration"]

    filenames = list(file_wise_durations.keys())
    durations = list(file_wise_durations.values())

    data = [
        go.Table(
            header=dict(
                values=["FileName", "Total Time Spent(seconds)"]
            ),  # noqa: E501
            cells=dict(values=[filenames, durations]),
        )
    ]  # noqa: E128

    # fig = go.Figure(data=data)
    # plot(fig,filename="table.html")

    fig.append_trace(data[0], 3, 1)
    ###############################
    plot(fig, filename=os.path.join(DATA_FOLDER_PATH, "analysis.html"))

    # my_dboard = dashboard.Dashboard()
    # my_dboard.get_preview()


show_graphs()
