from flask import Flask, send_from_directory, jsonify
import numpy as np
from analyse import data, transform

app = Flask(__name__)

@app.route("/")
def base():
    return send_from_directory('client/dist', 'index.html')

# Path for all the static files (compiled JS/CSS, etc.)
@app.route("/<path:path>")
def home(path):
    return send_from_directory('client/dist', path)

from flask import request

from flask import request

@app.route("/ticker", methods=['POST'])
def get_ticker():
    req_data = request.get_json()  # This will return a dictionary
    ticks = req_data['ticks']  # Access the 'ticks' value from the dictionary
    ticker = req_data["ticker"]
    interval = req_data["interval"]

    df = data.get_binance_candlestick(ticker, interval)
    transform.batch_insert_ema(df, ticks)
    transform.batch_insert_momentum_oscilator(df, ticks)

    # df = df.dropna(axis="index")

    # df["datetime"] = df.astype(np.int64) // 10**9
    res = df.to_json(orient="records")
    return res

if __name__ == "__main__":
    app.run(debug=True)