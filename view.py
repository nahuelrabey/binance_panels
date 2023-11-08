import time
import threading
from alerts import check_1m, check_15m, check_1h
from main import get_tickers
from flask import Flask

TICKERS = get_tickers()
HOST = "localhost"
PORT = 8001
app = Flask(__name__)

@app.route("/")
def hello_world():
    content = ""
    with open("./view.html", "r") as file:
        content = file.readlines()
        content = "</br>".join(content)

    return "<p>"+content+"<p>"

if __name__ == '__main__':

    app.run(debug=True, port=PORT, host=HOST)
