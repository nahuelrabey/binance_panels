import pandas as pd
from typing import Tuple
from analyse import data, transform
from .position import Position
from .base import get_ticker_last_data

def calculate_indicators(ticker: pd.DataFrame) -> Tuple[float, float]:
    short: int = 12
    long: int = 26
    signal: int = 9

    transform.insert_macd_oscilator(ticker, short, long, signal)

    macd_ema_id: str = transform.macd_ema_id(short, long, signal)
    macd_id: str = transform.macd_id(short, long, signal)

    last_macd: float = ticker[macd_id].iloc[-1]
    last_ema_macd: float = ticker[macd_ema_id].iloc[-1]

    return last_macd, last_ema_macd

def buy_macd_condtion(last_macd, last_ema_macd):
    macd_positive = last_macd > 0
    ema_macd_positive = last_ema_macd > 0
    macd_above_ema_macd = last_macd > last_ema_macd

    return macd_above_ema_macd and macd_positive and ema_macd_positive


def macd(ticker: pd.DataFrame, position: Position, verbose=False):

    last_price, last_datetime = get_ticker_last_data(ticker)
    last_macd, last_ema_macd = calculate_indicators(ticker)

    if (buy_macd_condtion(last_macd, last_ema_macd)):
        if (position.is_traded()):
            return last_datetime, last_price, last_macd, last_ema_macd 

        position.founds -= position.max_trade
        position.coin_traded += position.max_trade / last_price
        position.traded += position.max_trade

        if (verbose):
            print("\n\tBUY")
            position.print_buy_table(last_price)

    # if (check_sell_condition(last_ema_macd, last_macd, last_momentum)):
    if (not buy_macd_condtion(last_ema_macd, last_macd)):
        if (position.coin_traded == 0):
            return last_datetime, last_price, last_macd, last_ema_macd 

        position.sell = position.coin_traded * last_price
        position.founds += position.sell
        position.coin_traded = 0
        position.traded = 0
        position.gained += position.sell - position.max_trade

        if (verbose):
            print("\n\tSELL")
            position.print_sell_table(last_price)

    return last_datetime, last_price, last_macd, last_ema_macd 