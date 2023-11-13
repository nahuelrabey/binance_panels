import pandas as pd
from typing import Tuple
from analyse import data, transform
from .position import Position
from .base import get_ticker_last_data, StrategyVariables, BaseStrategy

class MacdVariables(StrategyVariables):
    def __init__(self, last_datetime:float, last_price: float, last_macd: float, last_ema_macd: float):
        self.last_datetime = last_datetime
        self.last_price = last_price
        self.last_macd = last_macd
        self.last_ema_macd = last_ema_macd
    
    def print(self) -> None:
        print(f"{'datetime':<15}{'Last Price':<15}{'Last MACD':<15}{'Last EMA MACD':<15}")
        print(f"{self.last_datetime:<15.2f}{self.last_price:<15.2f}{self.last_macd:<15.2f}{self.last_ema_macd:<15.2f}")

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

def buy_macd_condtion(variables: MacdVariables) -> bool:
    macd_positive = variables.last_macd > 0
    ema_macd_positive = variables.last_ema_macd > 0
    macd_above_ema_macd = variables.last_macd > variables.last_ema_macd

    return macd_above_ema_macd and macd_positive and ema_macd_positive

class Strategy(BaseStrategy):
    def __init__(self, ticker_name: str, position: Position, verbose=False):
        self.ticker_name = ticker_name
        self.position = position
        self.verbose = verbose
    
    def execute(self, ticker_data: pd.DataFrame) -> MacdVariables:
        last_price, last_datetime = get_ticker_last_data(ticker_data)
        last_macd, last_ema_macd = calculate_indicators(ticker_data)

        variables = MacdVariables(last_datetime, last_price, last_macd, last_ema_macd)

        if (buy_macd_condtion(variables)):
            if (self.position.is_traded()):
                return variables

            self.position.founds -= self.position.max_trade
            self.position.coin_traded += self.position.max_trade / last_price
            self.position.traded += self.position.max_trade
        
        if (not buy_macd_condtion(variables)):
            if (self.position.coin_traded == 0):
                return variables

            self.position.sell = self.position.coin_traded * last_price
            self.position.founds += self.position.sell
            self.position.coin_traded = 0
            self.position.traded = 0
            self.position.gained += self.position.sell - self.position.max_trade
    
        return variables
    
    def create_pandas(self = None) -> pd.DataFrame:
        return pd.DataFrame(columns=["datetime", "founds", "coin_traded", "traded", "gained", "max_trade", "last_price", "last_macd", "last_ema_macd"])
    
    def save_to_pandas(self, variables: MacdVariables,data: pd.DataFrame):
        new_row = {
            "datetime": variables.last_datetime,
            "founds": self.position.founds,
            "coin_traded": self.position.coin_traded,
            "traded": self.position.traded,
            "gained": self.position.gained,
            "max_trade": self.position.max_trade,
            "last_price": variables.last_price,
            "last_macd": variables.last_macd,
            "last_ema_macd": variables.last_ema_macd,
        }
        data.loc[len(data)] = new_row