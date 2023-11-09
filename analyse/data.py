import pandas as pd
from binance.spot import Spot

client = Spot()

def get_tickers():
    return [
        "BTCUSDT",
        "ETHUSDT",
        "SOLUSDT",
        "XRPUSDT",
        "DOGEUSDT",
        "ADAUSDT",
        "BNBUSDT",
        "LINKUSDT",
        "MATICUSDT"
    ]

def get_binance_candlestick(ticker:str, interval:str = "1m") -> pd.DataFrame:
    """
    Retrieves financial data for a specific stock ticker and returns it as a pandas DataFrame.

    Parameters:
    ticker (str): The stock symbol to retrieve data for.
    interval (str, optional): The interval at which to retrieve data. Defaults to "1m" (one minute).

    Returns:
    pd.DataFrame: A DataFrame containing the financial data for the specified stock ticker. The DataFrame includes the following columns: "OpenTime", "Open", "High", "Low", "Close", "Volume", "CloseTime", and "datetime". The "datetime" column is the "CloseTime" column converted from milliseconds to a datetime object.
    """
    res = client.klines(symbol=ticker, interval=interval)
    df = pd.DataFrame(res, columns=["OpenTime","Open","High","Low","Close","Volume","CloseTime","Quote","Trades","TakerBaseVolume","TakerQuoteVolume","nan"])
    df = df[["OpenTime","Open","High","Low","Close","Volume","CloseTime"]]
    df = df.astype({"Open":'float', "High":"float", "Low":"float","Close":"float","Volume":"float"})
    df["datetime"] = pd.to_datetime(df["CloseTime"], unit="ms" )
    return df