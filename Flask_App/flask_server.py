import requests
from flask import request, Flask, jsonify, render_template, redirect, url_for
import mysql.connector
import sql_actions
import datetime
import uuid
import matplotlib.pyplot as plt
from flask_bootstrap import Bootstrap
from forms import signupForm
import os


db = mysql.connector.connect(host='localhost', database='code_time', user='root', password='codetime')
app = Flask(__name__)
bootstrap = Bootstrap(app)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


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


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = signupForm()
    # if user click submit on signup page
    if form.validate_on_submit():
        uid = form.uid.data
        print(uid)
        return redirect(url_for('dashboard', uid=uid))
    unique_id = uuid.uuid4()
    unique_id = str(unique_id)
    sql_actions.add_data_users(db, unique_id)
    return render_template('login.html', form=form)


@app.route('/dashboard/<uid>', methods=['GET'])
def dashboard(uid):
    chart_data = sql_actions.retrieve_data_table_chart(db, uid)
    bar_data = sql_actions.retrieve_data_pie_chart(db, uid)
    # [(user_id, file_name, start_date, end_date)]
    # Graph Plot Function
    x_left = []
    y_time = []
    # labels for bars
    tick_label = []
    return render_template('dashboard.html')
    # return render_template('dashboard.html')


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
