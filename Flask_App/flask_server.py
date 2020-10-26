from flask import request, Flask, render_template, redirect, url_for
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
        uid = form.uid.data
        print(uid)
        return redirect(url_for('dashboard', uid=uid))
    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET'])
def signup():
    unique_id = uuid.uuid4()
    unique_id = str(unique_id)
    sql_actions.add_data_users(db, unique_id)
    return_data = {"your_id": unique_id}
    return json.dumps(return_data)


@app.route('/dashboard/<uid>', methods=['GET'])
def dashboard(uid):
    time_data = sql_actions.retrieve_data_table_chart(db, uid)
    pie_chart_data = sql_actions.retrieve_data_pie_chart(db, uid)
    # [(user_id, file_name, start_date, end_date)]



    # Graph Plot Function
    """
    table_data = []
    for item in chart_data:
        table_data.append((item[1], float(item[2])))
    fig, axs = plt.subplots()
    collabel = ("File Name", "Time Spend")
    fig.patch.set_visible(False)
    axs.table(cellText=table_data, colLabels=collabel, loc='center')
    #plt.show()
    plt.savefig('static/table_chart.png')
    """
    pie_file_types = []
    pie_file_total = []
    
    # create pie chart
    for item in pie_chart_data:
        pie_file_types.append(item[1])
        pie_file_total.append(item[2])
    plt.figure(figsize=(10, 7))
    plt.pie(pie_file_total, labels=pie_file_types, autopct='%.2f')
    # show plot
    #plt.show()
    plt.savefig('static/pie_chart.png')
    
    return render_template('dashboard.html',title='Dashboard',pie_chart_data=pie_chart_data,time_data=time_data)
    # return render_template('dashboard.html')


@app.route('/send', methods=['POST'])
def send():
    send_list = request.get_json(force=True)
    print(send_list, type(send_list))
    sql_actions.add_data_dashboard(db, send_list['data'])
    return "Data added"


if __name__ == "__main__":
    server_ip = '0.0.0.0'
    server_port = 8080
    app.run(host=server_ip, port=server_port, debug=True)
