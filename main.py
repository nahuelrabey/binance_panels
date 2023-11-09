from flask import request
from flask import Flask, send_from_directory, jsonify
import numpy as np
from analyse import data, transform

app = Flask(__name__)


@app.route("/")
def base():
    return send_from_directory('client/dist', 'index.html')
# Path for all the static files (compiled JS/CSS, etc.)

@app.route("/assets/<path:path>")
def home(path):
    return send_from_directory('client/dist', f"assets/{path}")

@app.route("/page/<path:path>")
def pages(path):
    return send_from_directory('client/dist', f"index.html")

@app.route("/ticker/momentum", methods=['POST'])
def get_ticker_momentum():
    req_data = request.get_json()  # This will return a dictionary
    ticks = req_data['ticks']  # Access the 'ticks' value from the dictionary
    ticker = req_data["ticker"]
    interval = req_data["interval"]

    df = data.get_binance_candlestick(ticker, interval)
    transform.batch_insert_ema(df, ticks)
    transform.batch_insert_momentum_oscilator(df, ticks)

    res = df.to_json(orient="records")
    return res


@app.route("/ticker/macd", methods=['POST'])
def get_ticker_macd():
    req_data = request.get_json()  
    ticker = req_data["ticker"]
    interval = req_data["interval"]
    ticks = req_data['ticks']  
    short = req_data["short"]
    long = req_data["long"]
    signal = req_data["signal"]

    df = data.get_binance_candlestick(ticker, interval)
    transform.batch_insert_ema(df, ticks)
    transform.insert_macd_oscilator(df, short, long, signal)

    res = df.to_json(orient="records")
    return res

@app.route("/macd/id", methods=['POST'])
def get_macd_id():
    req_data = request.get_json()
    short = req_data["short"]
    long = req_data["long"]
    signal = req_data["signal"]

    return transform.macd_id(short, long, signal)

@app.route("/macd/ema-id", methods=['POST'])
def get_macd_ema_id():
    req_data = request.get_json()
    short = req_data["short"]
    long = req_data["long"]
    signal = req_data["signal"]

    return transform.macd_ema_id(short, long, signal)

if __name__ == "__main__":
    app.run(debug=True)
