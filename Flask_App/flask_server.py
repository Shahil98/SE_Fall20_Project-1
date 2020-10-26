from flask import request, Flask, render_template, redirect, url_for, flash
import mysql.connector
import sql_actions
import uuid
import matplotlib.pyplot as plt
from flask_bootstrap import Bootstrap
from forms import signupForm
import os
import json


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


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = signupForm()
    # if user click submit on signup page
    if form.validate_on_submit():
        some_id = form.uid.data
        uid = sql_actions.check_user(db,some_id)
        print(some_id)
        print(uid)
        if uid == -1:
            flash('This userID does not exist, Please try again','error')
            return redirect(url_for('login'))
        return redirect(url_for('dashboard', uid=some_id))
    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET'])
def signup():
    unique_id = uuid.uuid4()
    unique_id = str(unique_id)
    sql_actions.add_data_users(db, unique_id)
    #return_data = {"your_id": unique_id}
    return(unique_id)


@app.route('/dashboard/<uid>', methods=['GET'])
def dashboard(uid):
    # We query the database using two function(retrieve_data_table_chart and retrieve_data_pie_chart) in the sql_actions
    time_data = sql_actions.retrieve_data_table_chart(db, uid)
    number_of_files_data = sql_actions.retrieve_data_pie_chart(db, uid)
    # [(user_id, file_name, start_date, end_date)]
    pie_file_types = []
    pie_file_total = []

    # create pie chart
    for item in number_of_files_data:
        pie_file_types.append(item[1])
        pie_file_total.append(item[2])
    plt.figure(figsize=(10, 7))
    plt.pie(pie_file_total, labels=pie_file_types, autopct='%.2f')
    # show plot
    plt.savefig('static/number_of_files_pie_chart.png')

    total_time = 0
    file_type_times = sql_actions.retrieve_data_graph_chart(db, uid)
    file_type_names = []
    file_type_duration = []
    for i in range(len(file_type_times)):
        file_type_names.append(file_type_times[i][1])
        file_type_duration.append(file_type_times[i][2])
    plt.figure(figsize=(10, 7))
    plt.pie(file_type_duration, labels=file_type_names, autopct='%.2f')
    # show plot
    plt.savefig('static/file_type_duration_pie_chart.png')
    return render_template('dashboard.html', title='Dashboard', time_data=time_data)


@app.route('/send', methods=['POST'])
def send():
    send_list = request.get_json(force=True)
    sql_actions.add_data_dashboard(db, send_list['data'])
    return "Data added"


if __name__ == "__main__":
    server_ip = '0.0.0.0'
    server_port = 8080
    app.run(host=server_ip, port=server_port, debug=True)
