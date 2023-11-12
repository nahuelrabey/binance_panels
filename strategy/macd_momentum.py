import pandas as pd
from typing import Tuple
from analyse import transform
from .base import get_ticker_last_data
from .position import Position

def calculate_indicators(ticker: pd.DataFrame) -> Tuple[float, float, float]:
    short: int = 12
    long: int = 26
    signal: int = 9

    transform.insert_macd_oscilator(ticker, short, long, signal)

    macd_ema_id: str = transform.macd_ema_id(short, long, signal)
    macd_id: str = transform.macd_id(short, long, signal)

    last_macd: float = ticker[macd_id].iloc[-1]
    last_ema_macd: float = ticker[macd_ema_id].iloc[-1]

    transform.insert_momentum_oscilator(ticker, short)
    momentum_id: str = transform.momentum_id(short)
    last_momentum: float = ticker[momentum_id].iloc[-1]

    return last_macd, last_ema_macd, last_momentum

def buy_macd_momentum_condtion(last_macd:float, last_ema_macd:float, last_momentum:float):
    macd_positive = last_macd > 0
    ema_macd_positive = last_ema_macd > 0
    macd_above_ema_macd = last_macd > last_ema_macd
    momentum_above_one = last_momentum > 1

    return macd_above_ema_macd and macd_positive and ema_macd_positive and momentum_above_one

def macd_momentum(ticker: pd.DataFrame, position: Position, verbose=False):
    last_price, last_datetime = get_ticker_last_data(ticker)
    last_macd, last_ema_macd, last_momentum = calculate_indicators(ticker)

    if (buy_macd_momentum_condtion(last_macd, last_ema_macd, last_momentum)):
        if (position.is_traded()):
            return last_datetime, last_price, last_macd, last_ema_macd, last_momentum

        position.founds -= position.max_trade
        position.coin_traded += position.max_trade / last_price
        position.traded += position.max_trade

        if (verbose):
            print("\n\tBUY")
            position.print_buy_table(last_price)

    # if (check_sell_condition(last_ema_macd, last_macd, last_momentum)):
    if (not buy_macd_momentum_condtion(last_ema_macd, last_macd, last_momentum)):
        if (position.coin_traded == 0):
            return last_datetime, last_price, last_macd, last_ema_macd, last_momentum

        position.sell = position.coin_traded * last_price
        position.founds += position.sell
        position.coin_traded = 0
        position.traded = 0
        position.gained += position.sell - position.max_trade

        if (verbose):
            print("\n\tSELL")
            position.print_sell_table(last_price)

    return last_datetime, last_price, last_macd, last_ema_macd, last_momentum