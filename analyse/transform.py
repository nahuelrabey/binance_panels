import pandas as pd
from analyse import calculate 

"""
This module, 'transform', contains functions for inserting calculated financial indicators into a DataFrame.

Functions:
- insert_ema(df: pd.DataFrame, n: int) -> None: Inserts the Exponential Moving Average (EMA) values into a given DataFrame for a specified period.
- batch_insert_ema(df: pd.DataFrame, ticks: list[int]) -> pd.DataFrame: Inserts the EMA values into a given DataFrame for a list of specified periods.
- insert_momentum_oscilator(df: pd.DataFrame, n: int) -> pd.DataFrame: Inserts the momentum oscillator values into a given DataFrame for a specified period.
- batch_insert_momentum_oscilator(df: pd.DataFrame, ticks: list[int]) -> pd.DataFrame: Inserts the momentum oscillator values into a given DataFrame for a list of specified periods.

Each function takes a DataFrame containing stock data and a period (or list of periods) as parameters, and modifies the DataFrame to include a new column (or columns) containing the calculated values for the given indicator. The DataFrame must include a "Close" column, which represents the closing prices of the stock.
"""

def insert_ema(df: pd.DataFrame, n: int):
    """
    Inserts the Exponential Moving Average (EMA) values into a given DataFrame for a specified period.

    Parameters:
    df (pd.DataFrame): The DataFrame containing the stock data. It must include a "Close" column, which represents the closing prices of the stock.
    n (int): The number of periods for which to calculate the EMA. 

    Returns:
    pd.DataFrame: The DataFrame with a new column "{n}_ema" added, which contains the calculated EMA values for the given number of periods.
    """
    ema = calculate.ema(df, n)
    df[f"{n}_ema"] = ema

def batch_insert_ema(df: pd.DataFrame, ticks: list[int]):
    """
    Inserts the Exponential Moving Average (EMA) values into a given DataFrame for a list of specified periods.

    Parameters:
    df (pd.DataFrame): The DataFrame containing the stock data. It must include a "Close" column, which represents the closing prices of the stock.
    ticks (list[int]): A list of periods for which to calculate the EMA. Each period represents the number of most recent closing prices that should be considered in the calculation.

    Returns:
    pd.DataFrame: The original DataFrame, with new columns added for each period in ticks: "{n}_ema", which contains the calculated EMA values.
    """
    for tick in ticks:
        insert_ema(df, tick)

def insert_momentum_oscilator(df: pd.DataFrame, n: int):
    """
    Inserts the momentum oscillator values into a given DataFrame for a specified period.

    Parameters:
    df (pd.DataFrame): The DataFrame containing the stock data. It must include a "Close" column, which represents the closing prices of the stock.
    n (int): The period for which to calculate the momentum oscillator. This is the number of most recent closing prices that should be considered in the calculation.

    Returns:
    pd.DataFrame: The DataFrame with a new column "{n}_momentum" added, which contains the calculated momentum oscillator values.
    """
    momentum = calculate.momentum_oscilator(df, n)
    df[f"{n}_momentum"] = momentum

def batch_insert_momentum_oscilator(df: pd.DataFrame, ticks: list[int]):
    """
    Inserts the momentum oscillator values into a given DataFrame for a list of specified periods.

    Parameters:
    df (pd.DataFrame): The DataFrame containing the stock data. It must include a "Close" column, which represents the closing prices of the stock.
    ticks (list[int]): A list of periods for which to calculate the momentum oscillator. Each period represents the number of most recent closing prices that should be considered in the calculation.

    Returns:
    pd.DataFrame: The DataFrame with new columns added for each period in ticks: "{n}_momentum", which contains the calculated momentum oscillator values.
    """

    for tick in ticks:
        insert_momentum_oscilator(df, tick)

def macd_id(short: int, long: int, signal: int):
    return f"{short}_{long}_{signal}_macd"
def macd_ema_id(short: int, long: int, signal: int):
    return f"{short}_{long}_{signal}_signal"
def insert_macd_oscilator(df: pd.DataFrame, short: int, long: int, signal: int):
    """
    Inserts the MACD oscillator values into a given DataFrame for a specified period.

    Parameters:
    df (pd.DataFrame): The DataFrame containing the stock data. It must include a "Close" column, which represents the closing prices of the stock.
    short (int): The period for which to calculate the short-term EMA. This is the number of most recent closing prices that should be considered in the calculation.
    long (int): The period for which to calculate the long-term EMA. This is the number of most recent closing prices that should be considered in the calculation.
    signal (int): The period for which to calculate the signal line. This is the number of most recent closing prices that should be considered in the calculation.

    Returns:
    pd.DataFrame: The DataFrame with new columns added: "macd", which contains the calculated MACD oscillator values, and "signal", which contains the calculated signal line values.
    """
    macd, ema_macd = calculate.macd_exponential(df, short, long, signal)
    df[macd_id(short, long, signal)] = macd
    df[macd_ema_id(short, long, signal)] = ema_macd 