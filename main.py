import pandas as pd
from datetime import timedelta
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

def get_data_as_df(ticker:str, interval:str = "1m") -> pd.DataFrame:
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

def create_ema(df:pd.DataFrame, n:int) -> pd.DataFrame:
    """
    Calculates the Exponential Moving Average (EMA) for a given DataFrame and period, and adds it as a new column to the DataFrame.

    Parameters:
    df (pd.DataFrame): The DataFrame containing the stock data. It must include a "Close" column, which represents the closing prices of the stock.
    n (int): The period for which to calculate the EMA. This is the number of most recent closing prices that should be considered in the calculation.

    Returns:
    pd.DataFrame: The original DataFrame, with two new columns added: "{n}_ema", which contains the calculated EMA values, and "delta_{n}_ema", which contains the percentage change in the EMA from the previous period.
    """
    close = df["Close"]
    ema = close.ewm(span=n, adjust=False).mean()
    delta_ema = ema - ema.shift(n)
    df[f"{n}_ema"] = ema
    df[f"delta_{n}_ema"] = (delta_ema / ema)*100

    return df

def batch_create_emas(df:pd.DataFrame, ticks:list[int]):
    for t in ticks:
        df = create_ema(df, t)
    
    return df 

def momentum_oscilator(data:pd.DataFrame, n: int):
    price = data["Close"]
    momentum = price / price.shift(n)
    return momentum

def create_momentum_oscilator(data: pd.DataFrame, n:int):
    momentum = momentum_oscilator(data,n)
    data[f"{n}_momentum"] = momentum
    return data

def batch_create_momentum_oscilators(data: pd.DataFrame, ticks:list[int]):
    for t in ticks:
        data = create_momentum_oscilator(data, t)
    return data

def price_difference(df: pd.DataFrame, n):
    close = df["Close"]
    diff = close - close.shift(n)
    delta_diff = (diff / close)*100
    df[f"{n}_diff"] = diff
    df[f"delta_{n}_diff"] = delta_diff
    return df

def span_30_minutes(df:pd.DataFrame):
    datetime = df["datetime"]
    span = timedelta(minutes=30)
    return df[df["datetime"] > datetime - span]



# def find_ideal_markets(tickers: 'list[str]', interval:str, tick):
#     # tickers = ["BTCUSDT","ETHUSDT","SOLUSDT","XRPUSDT"]
#     res: 'list[list[str,pd.DataFrame]]' = []
#     for ticker in tickers:
#         df = get_data_as_df(ticker,interval)
#         df = create_ema(df, tick)
#         last = df.iloc[-1]
#         last_close = last["Close"]
#         last_ema = last[f"{tick}_ema"]
#         if (last_close>last_ema):
#             res.append((ticker, df))
#             print(f"ticker: {ticker}, close: {last_close}, ema: {last_ema}")
    
#     return res
