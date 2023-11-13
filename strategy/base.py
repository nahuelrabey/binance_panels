import time
import pandas as pd
from typing import Tuple, Callable
from analyse import data
from .position import Position
from abc import ABCMeta
import traceback

def get_ticker_last_data(ticker_data: pd.DataFrame) -> Tuple[float, pd.Timestamp]:
    last_price: float = ticker_data["Close"].iloc[-1]
    last_datetime: pd.Timestamp = ticker_data["datetime"].iloc[-1]
    return last_price, last_datetime

def log(ticker_name: str, text: str):
    with open(f"{ticker_name}_log.txt", "a") as file:
        file.write(text + "\n")
        file.write("-"*50 + "\n")

class StrategyVariables(metaclass=ABCMeta):
    def print() -> None:
        pass

class BaseStrategy(metaclass=ABCMeta):
    def execute(self, ticker: pd.DataFrame) -> StrategyVariables:
        pass
    def create_pandas()-> pd.DataFrame:
        pass
    def save_to_pandas(self, variables: StrategyVariables, data: pd.DataFrame):
        pass 
    def save_to_csv(self, fileName='output.csv'):
        pass

# type Strategy = Callable[[pd.DataFrame, Position, bool], StrategyVariables]

def run(ticker_name: str, position: Position, strategy: BaseStrategy):

    ticker = data.get_binance_candlestick(ticker_name)
    variables = strategy(
        ticker_name, ticker)

    variables.print()
    variables.save_to_csv(position) 


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
