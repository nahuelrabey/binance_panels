from pandas import Series
import pandas as pd

"""
This module contains functions for calculating various financial indicators.

Functions:
- ema(df: pd.DataFrame, n: int) -> pd.Series: Calculates the Exponential Moving Average (EMA) for a given DataFrame and period.
- momentum_oscilator(data: pd.DataFrame, n: int) -> pd.Series: Calculates the momentum oscillator for a given DataFrame and period.
- price_difference(df: pd.DataFrame, n: int) -> pd.Series: Calculates the price difference for a given DataFrame and period.

Each function takes a DataFrame containing stock data and a period as parameters, and returns a Series containing the calculated values for the given indicator. The DataFrame must include a "Close" column, which represents the closing prices of the stock.
"""


def __validates_df(df: pd.DataFrame) -> None:
    # check that "Close" column exists
    if "Close" not in df.columns:
        raise ValueError("DataFrame must include a 'Close' column")


def ema(df: pd.DataFrame, n: int) -> pd.Series:
    """
    Calculates the Exponential Moving Average (EMA) for a given DataFrame and period.

    Parameters:
    df (pd.DataFrame): The DataFrame containing the stock data. It must include a "Close" column, which represents the closing prices of the stock.
    n (int): The number of periods for which to calculate the EMA. 

    Returns:
    pd.Series: A Series containing the calculated EMA values for the given number of periods.
    """

    __validates_df(df)

    close = df["Close"]
    ema = close.ewm(span=n, adjust=False).mean()
    return ema


def momentum_oscilator(df: pd.DataFrame, n: int) -> pd.Series:
    """
    Calculates the momentum oscillator for a given DataFrame and period.

    Parameters:
    data (pd.DataFrame): The DataFrame containing the stock data. It must include a "Close" column, which represents the closing prices of the stock.
    n (int): The period for which to calculate the momentum oscillator. This is the number of most recent closing prices that should be considered in the calculation.

    Returns:
    pd.Series: A Series containing the calculated momentum oscillator values.
    """
    __validates_df(df)

    price = df["Close"]
    momentum = price / price.shift(n)
    return momentum


def price_difference(df: pd.DataFrame, n: int) -> pd.Series:
    """
    Calculates the price difference for a given DataFrame and period.

    Parameters:
    df (pd.DataFrame): The DataFrame containing the stock data. It must include a "Close" column, which represents the closing prices of the stock.
    n (int): The period for which to calculate the price difference. This is the number of most recent closing prices that should be considered in the calculation.

    Returns:
    pd.Series: A Series containing the calculated price difference values for the given number of periods.
    """
    __validates_df(df)

    close = df["Close"]
    diff = close - close.shift(n)
    return diff


def macd_exponential(df: pd.DataFrame, short: int, long: int, signal: int) -> tuple[Series, Series]:
    """
    Calculate the MACD (Moving Average Convergence Divergence) and the signal line.

    Parameters:
    df (pd.DataFrame): The input data frame.
    short (int): The short period for EMA calculation.
    long (int): The long period for EMA calculation.
    signal (int): The period for signal line calculation.

    Returns:
    Tuple[Series, Series]: A tuple containing the MACD and the signal line as pandas Series.
    """

    short_ema = ema(df, short)
    long_ema = ema(df, long)
    macd = short_ema - long_ema
    ema_macd = macd.ewm(span=signal, adjust=False).mean()
    return (macd, ema_macd)
