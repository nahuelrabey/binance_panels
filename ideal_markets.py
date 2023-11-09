import pandas as pd
from analyse import data, transform

def by_upper_ema(tickers: 'list[str]', interval:str, tick):
    # tickers = ["BTCUSDT","ETHUSDT","SOLUSDT","XRPUSDT"]
    res: 'list[list[str,pd.DataFrame]]' = []
    for ticker in tickers:
        df = data.get_binance_candlestick(ticker, interval)
        transform.insert_ema(df, tick)
        last = df.iloc[-1]
        last_close = last["Close"]
        last_ema = last[f"{tick}_ema"]
        if (last_close>last_ema):
            res.append((ticker, df))
            print(f"ticker: {ticker}, close: {last_close}, ema: {last_ema}")
    
    return res


def are_ordered(int_list:list[int]):
    for i in range(1,len(int_list)):
        if (int_list[i-1] > int_list[i]):
            return False 
    return True

def are_greater_or_equal(float_list:list[float]):
    for i in range(1, len(float_list)):
        if (not (float_list[i-1]>=float_list[i])):
            return False
    return True

type TickerDataTouple = list[str, pd.DataFrame]
def by_crossing_emas(tickers: 'list[str]', interval:str, ticks: 'list[int]'):
    res: 'list[TickerDataTouple]' = []

    if(not are_ordered(ticks)):
        raise ValueError("ticks list must be ordered")

    for ticker in tickers:
        # df = get_data_as_df(ticker,interval)
        df = data.get_binance_candlestick(ticker, interval)
        last_emas = []
        # last_close = df["Close"].iloc[-1]
        
        for t in ticks:
            transform.insert_ema(df, t)
            last_ema = df[f"{t}_ema"].iloc[-1]
            last_emas.append(last_ema)

        if (are_greater_or_equal(last_emas)):
            res.append((ticker, df))

    return res

def by_momentum_oscilator(tickers:'list[str]', interval:str, tick:int):
    res: 'list[TickerDataTouple]' = []

    for ticker in tickers:
        df = data.get_binance_candlestick(ticker, interval)
        transform.insert_momentum_oscilator(df, tick)
        last_momentum = df[f"{tick}_momentum"].iloc[-1]
        if last_momentum > 1:
            res.append([ticker, data])
    
    return res
