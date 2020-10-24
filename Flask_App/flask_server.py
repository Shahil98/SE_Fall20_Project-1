import requests
from flask import request, Flask, jsonify, render_template
import mysql.connector
import sql_actions
import datetime
import uuid
import matplotlib.pyplot as plt

db = mysql.connector.connect(host='localhost', database='code_time', user='root', password='codetime')

app = Flask(__name__)


@app.route("/")
def index():
    """
    Function to render index.html when a request is made to "/".
    """

    return render_template("index.html", title="Code Time")


@app.route("/insert_data", methods=["post"])
def insert_data():
    data = request.get_json()
    print(data)
    return render_template("index.html", title="Code Time")


@app.route('/signup', methods=['GET'])
def signup():
    unique_id = uuid.uuid4()
    unique_id = str(unique_id)
    sql_actions.add_data_users(db, unique_id)
    return_id = {"your_id": unique_id}
    return return_id


@app.route('/dashboard/<user_id>', methods=['GET'])
def dashboard(db, user_id):
    display_data = sql_actions.retrieve_data(db, user_id)
    # [(user_id, file_name, start_date, end_date)]
    # Graph Plot Function
    x_left = []
    y_time = []
    # labels for bars
    tick_label = []
    for i in range(len(display_data)):
        x_left.append(i)
        y_time.append(display_data[i][3])
        tick_label.append(display_data[i][1])
    plt.bar(x_left, y_time, tick_label=tick_label, width=0.8, color=['red', 'green'])
    plt.xlabel('Files')
    plt.ylabel('Time Worked')
    plt.title(display_data[0][0])
    plt.savefig('static/images/plot.png')
    return render_template('plot.html', url='/static/images/plot.png')


@app.route('/send', methods=['POST'])
def send(db, user_id):
    send_list = request.get_json(force=True)
    print(send_list)
    send_list = send_list.get_json()
    sql_actions.add_data_dashboard(db, send_list)


if __name__ == "__main__":
    server_ip = '0.0.0.0'
    server_port = 8080
    app.run(host=server_ip, port=server_port, debug=True)
