from flask import Flask, render_template, request, send_file

app = Flask(__name__)


@app.route("/")
def index():
    """
    Function to render index.html when a request is made to "/".
    """

    return render_template("index.html", title="Code Time")
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8080)
