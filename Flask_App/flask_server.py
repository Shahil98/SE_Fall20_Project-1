import requests
from flask import request, Flask, jsonify, render_template
import mysql.connector
import sql_actions
import datetime
import uuid

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
    sql_actions.add_data_users(db, unique_id)
    return unique_id


@app.route('/dashboard/<user_id>', methods=['GET'])
def dashboard(db, user_id):
    display_data = sql_actions.retrieve_data(db, user_id)
    # matplotlib function
    return display_data


@app.route('/send', methods=['POST'])
def send(db, user_id):
    send_list = request.get_json(force=True)
    print(send_list)
    sql_actions.add_data_dashboard(db, send_list)


if __name__ == "__main__":
    try:
        db = mysql.connector.connect(host='localhost', database='code_time', user='root', password='codetime')
    except mysql.connector.Error as e:
        print(e)
    server_ip = '0.0.0.0'
    server_port = '8080'
    app.run(host=server_ip, port=server_port, debug=True)
