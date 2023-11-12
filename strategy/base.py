import time
import pandas as pd
from typing import Tuple, Callable
from analyse import data
from .position import Position
import traceback

def print_variables(last_price, last_macd, last_ema_macd, last_momentum):
    """
    Prints the provided values as a table.

    Parameters:
    founds (float): The remaining founds after the trade.
    btc (float): The btc value after the trade.
    traded (float): The total amount traded after the trade.
    max_trade (float): The maximum trade value.
    last_price (float): The last price value.

    Returns:
    None
    """
    print(f"{'Last Price':<15}{'Last MACD':<15}{
          'Last EMA MACD':<15}{'Last Momentum':<15}")
    print(f"{last_price:<15.2f}{last_macd:<15.2f}{
          last_ema_macd:<15.2f}{last_momentum:<15.4f}")


def get_ticker_last_data(ticker_data: pd.DataFrame) -> Tuple[float, pd.Timestamp]:
    last_price: float = ticker_data["Close"].iloc[-1]
    last_datetime: pd.Timestamp = ticker_data["datetime"].iloc[-1]
    return last_price, last_datetime


# def calculate_indicators(ticker: pd.DataFrame) -> Tuple[float, float, float]:
#     short: int = 12
#     long: int = 26
#     signal: int = 9

#     transform.insert_macd_oscilator(ticker, short, long, signal)

#     macd_ema_id: str = transform.macd_ema_id(short, long, signal)
#     macd_id: str = transform.macd_id(short, long, signal)

#     last_macd: float = ticker[macd_id].iloc[-1]
#     last_ema_macd: float = ticker[macd_ema_id].iloc[-1]

#     transform.insert_momentum_oscilator(ticker, short)
#     momentum_id: str = transform.momentum_id(short)
#     last_momentum: float = ticker[momentum_id].iloc[-1]

#     return last_macd, last_ema_macd, last_momentum


# def buy_macd_condtion(last_macd, last_ema_macd):
#     macd_positive = last_macd > 0
#     ema_macd_positive = last_ema_macd > 0
#     macd_above_ema_macd = last_macd > last_ema_macd

#     return macd_above_ema_macd and macd_positive and ema_macd_positive

# def buy_macd_momentum_condtion(last_macd:float, last_ema_macd:float, last_momentum:float):
#     macd_positive = last_macd > 0
#     ema_macd_positive = last_ema_macd > 0
#     macd_above_ema_macd = last_macd > last_ema_macd
#     momentum_above_one = last_momentum > 1

#     return macd_above_ema_macd and macd_positive and ema_macd_positive and momentum_above_one

# def strategy_macd(ticker: pd.DataFrame, position: Position, verbose=False):

#     last_price, last_datetime = get_ticker_last_data(ticker)
#     last_macd, last_ema_macd, last_momentum = calculate_indicators(ticker)

#     if (buy_macd_condtion(last_macd, last_ema_macd)):
#         if (position.is_traded()):
#             return last_datetime, last_price, last_macd, last_ema_macd, last_momentum

#         position.founds -= position.max_trade
#         position.coin_traded += position.max_trade / last_price
#         position.traded += position.max_trade

#         if (verbose):
#             print("\n\tBUY")
#             position.print_buy_table(last_price)

#     # if (check_sell_condition(last_ema_macd, last_macd, last_momentum)):
#     if (not buy_macd_condtion(last_ema_macd, last_macd)):
#         if (position.coin_traded == 0):
#             return last_datetime, last_price, last_macd, last_ema_macd, last_momentum

#         position.sell = position.coin_traded * last_price
#         position.founds += position.sell
#         position.coin_traded = 0
#         position.traded = 0
#         position.gained += position.sell - position.max_trade

#         if (verbose):
#             print("\n\tSELL")
#             position.print_sell_table(last_price)

#     return last_datetime, last_price, last_macd, last_ema_macd, last_momentum

# def strategy_macd_momentum(ticker: pd.DataFrame, position: Position, verbose=False):
#     last_price, last_datetime = get_ticker_last_data(ticker)
#     last_macd, last_ema_macd, last_momentum = calculate_indicators(ticker)

#     if (buy_macd_momentum_condtion(last_macd, last_ema_macd, last_momentum)):
#         if (position.is_traded()):
#             return last_datetime, last_price, last_macd, last_ema_macd, last_momentum

#         position.founds -= position.max_trade
#         position.coin_traded += position.max_trade / last_price
#         position.traded += position.max_trade

#         if (verbose):
#             print("\n\tBUY")
#             position.print_buy_table(last_price)

#     # if (check_sell_condition(last_ema_macd, last_macd, last_momentum)):
#     if (not buy_macd_momentum_condtion(last_ema_macd, last_macd, last_momentum)):
#         if (position.coin_traded == 0):
#             return last_datetime, last_price, last_macd, last_ema_macd, last_momentum

#         position.sell = position.coin_traded * last_price
#         position.founds += position.sell
#         position.coin_traded = 0
#         position.traded = 0
#         position.gained += position.sell - position.max_trade

#         if (verbose):
#             print("\n\tSELL")
#             position.print_sell_table(last_price)

#     return last_datetime, last_price, last_macd, last_ema_macd, last_momentum

# def log(ticker_name: str, text: str):
#     with open(f"{ticker_name}_log.txt", "a") as file:
#         file.write(text + "\n")
#         file.write("-"*50 + "\n")

type Strategy = Callable[[pd.DataFrame, Position, bool], list]

def run(ticker_name: str, position: Position, strategy: Strategy):

    ticker = data.get_binance_candlestick(ticker_name)
    last_datetime, last_price, last_macd, last_ema_macd, last_momentum = strategy(
        ticker_name, ticker)

    print(f"\n\tVariables {last_datetime}")
    print_variables(last_price, last_macd, last_ema_macd, last_momentum)
    position.save_to_csv(last_datetime, last_price,
                         last_ema_macd, last_macd, last_momentum)


if (__name__ == "__main__"):
    ticker_name = input("Please enter the ticker name: ")

    position = Position()

    while True:
        try:
            position.print_table()
            run(ticker_name, position)
            time.sleep(5)
        except Exception as e:
            tb_str = traceback.format_exc()
            log(ticker_name, tb_str)
            print(tb_str)
            time.sleep(5)
            continue
