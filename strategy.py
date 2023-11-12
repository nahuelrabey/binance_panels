import time
import pandas as pd
from typing import Tuple
from analyse import data, transform
import csv
import traceback


class Position:
    def __init__(self):
        self._founds = 50
        self._coin_traded = 0
        self._traded = 0
        self._gained = 0
        self._max_trade = 20
        self._last_price = 0

    @property
    def founds(self):
        return self._founds

    @founds.setter
    def founds(self, value):
        self._founds = value

    @property
    def coin_traded(self):
        return self._coin_traded

    @coin_traded.setter
    def coin_traded(self, value):
        self._coin_traded = value

    @property
    def traded(self):
        return self._traded

    @traded.setter
    def traded(self, value):
        self._traded = value

    @property
    def gained(self):
        return self._gained

    @gained.setter
    def gained(self, value):
        self._gained = value

    @property
    def max_trade(self):
        return self._max_trade

    @max_trade.setter
    def max_trade(self, value):
        self._max_trade = value

    @property
    def last_price(self):
        return self._last_price

    @last_price.setter
    def last_price(self, value):
        self._last_price = value

    def is_traded(self):
        return self.traded >= self.max_trade

    def print_table(self, last_price: float):
        print(f"{'Founds':<10}{'Traded':<10}{'Gained':<10}{
            'Max Trade':<10}{'Coin Traded':<10}{'COIN-USDT':<10}")
        print(f"{self.founds:<10.2f}{self.traded:<10.2f}{self.gained:<10.2f}{
            self.max_trade:<10.2f}{self.coin_traded:<10.2e}{self.coin_traded*last_price:<10.2f}")

    def print_buy_table(self, last_price: float):
        print(f"{'Founds':<10}{'COIN':<10}{'Traded':<10}{
              'Max Trade':<10}{'Last Price':<10}")
        print(f"{self.founds:<10.2f}{self.coin_traded:<10.2f}{
              self.traded:<10.2f}{self.max_trade:<10.2f}{last_price:<10.2f}")

    def print_sell_table(self, last_price: float):
        print(f"{'Sell':<10}{'Founds':<10}{
              'COIN':<10}{'Traded':<10}{'Gained':<10}")
        print(f"{self.founds:<10.2f}{self.coin_traded:<10.2f}{
              self.traded:<10.2f}{self.gained:<10.2f}{last_price:<10.2f}")

    def save_to_csv(self, last_date: pd.Timestamp, last_price: float, last_ema_macd: float, last_macd: float, last_momentum: float, fileName='output.csv'):
        with open(fileName, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([last_date, self.founds, self.coin_traded, self.traded, self.gained,
                            self.max_trade, last_price, last_ema_macd, last_macd, last_momentum])

    def save_to_dataframe(self, last_date: pd.Timestamp, last_price: float, last_ema_macd: float, last_macd: float, last_momentum: float, dataframe: pd.DataFrame):
        new_row = {"datetime": last_date, "founds": self.founds,
                   "coin_traded": self.coin_traded, "traded": self.traded, "gained": self.gained,
                   "max_trade": self.max_trade, "last_price": last_price, "last_ema_macd": last_ema_macd,
                   "last_macd": last_macd, "last_momentum": last_momentum}
        dataframe.loc[len(dataframe)] = new_row


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


def get_ticker_data(ticker: pd.DataFrame) -> Tuple[float, pd.Timestamp]:
    last_price: float = ticker["Close"].iloc[-1]
    last_datetime: pd.Timestamp = ticker["datetime"].iloc[-1]
    return last_price, last_datetime


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


def buy_macd_condtion(last_macd, last_ema_macd):
    # macd_positive = last_macd > 0
    # ema_macd_positive = last_ema_macd > 0
    macd_above_ema_macd = last_macd > last_ema_macd

    return macd_above_ema_macd



# def check_sell_condition(last_macd, last_ema_macd, last_momentum):
#     macd_positive = last_macd > 0
#     ema_macd_positive = last_ema_macd > 0
#     macd_above_ema_macd = last_macd > last_ema_macd
#     momentum_above_one = last_momentum > 1

#     return not macd_positive or not ema_macd_positive or not macd_above_ema_macd or not momentum_above_one


def strategy_macd(ticker: pd.DataFrame, position: Position, verbose=False):

    last_price, last_datetime = get_ticker_data(ticker)
    last_macd, last_ema_macd, last_momentum = calculate_indicators(ticker)

    if (buy_macd_condtion(last_macd, last_ema_macd)):
        if (position.is_traded()):
            return last_datetime, last_price, last_macd, last_ema_macd, last_momentum

        position.founds -= position.max_trade
        position.coin_traded += position.max_trade / last_price
        position.traded += position.max_trade

        if (verbose):
            print("\n\tBUY")
            position.print_buy_table(last_price)

    # if (check_sell_condition(last_ema_macd, last_macd, last_momentum)):
    if (not buy_macd_condtion(last_ema_macd, last_macd)):
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


def log(ticker_name: str, text: str):
    with open(f"{ticker_name}_log.txt", "a") as file:
        file.write(text + "\n")
        file.write("-"*50 + "\n")


def run(ticker_name: str, position: Position):

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
