import pandas as pd
from typing import Tuple
from analyse import transform
from .base import get_ticker_last_data, StrategyVariables, BaseStrategy 
from .position import Position

class MacdMomentumVariables(StrategyVariables):
    def __init__(self, last_datetime: float, last_price: float, last_macd: float, last_ema_macd: float, last_momentum: float):
        self.last_datetime = last_datetime
        self.last_price = last_price
        self.last_macd = last_macd
        self.last_ema_macd = last_ema_macd
        self.last_momentum = last_momentum

    def print(self):
        print(f"{'Last Price':<15}{'Last MACD':<15}{'Last EMA MACD':<15}{'Last Momentum':<15}")
        print(f"{self.last_price:<15.2f}{self.last_macd:<15.2f}{self.last_ema_macd:<15.2f}{self.last_momentum:<15.4f}")



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


def buy_macd_momentum_condtion(variables: MacdMomentumVariables) -> bool:
    macd_positive = variables.last_macd > 0
    ema_macd_positive = variables.last_ema_macd > 0
    macd_above_ema_macd = variables.last_macd > variables.last_ema_macd
    momentum_above_one = variables.last_momentum > 1

    return macd_above_ema_macd and macd_positive and ema_macd_positive and momentum_above_one

class Strategy(BaseStrategy):
    def __init__(self, position: Position, verbose=False):
        # self.ticker_data = ticker_data
        self.position = position
        self.verbose = verbose
        # self.variables: MacdMomentumVariables | None = None
    
    def execute(self, ticker: pd.DataFrame) -> MacdMomentumVariables:
        last_price, last_datetime = get_ticker_last_data(ticker)
        last_macd, last_ema_macd, last_momentum = calculate_indicators(ticker)
        variables = MacdMomentumVariables(last_datetime, last_price, last_macd, last_ema_macd, last_momentum)
        
        if (buy_macd_momentum_condtion(variables)):
            if (self.position.is_traded()):
                return variables

            self.position.founds -= self.position.max_trade
            self.position.coin_traded += self.position.max_trade / last_price
            self.position.traded += self.position.max_trade
        
        if (not buy_macd_momentum_condtion(variables)):
            if (self.position.coin_traded == 0):
                return variables

            self.position.sell = self.position.coin_traded * last_price
            self.position.founds += self.position.sell
            self.position.coin_traded = 0
            self.position.traded = 0
            self.position.gained += self.position.sell - self.position.max_trade
        
        return variables
    
    def create_pandas(self = None) -> pd.DataFrame:
        return pd.DataFrame(columns=["datetime", "founds", "coin_traded", "traded", "gained", "max_trade", "last_price", "last_macd", "last_ema_macd", "last_momentum"])

    def save_to_pandas(self, variables:MacdMomentumVariables, data: pd.DataFrame):
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
            "last_momentum": variables.last_momentum
        }

        data.loc[len(data)] = new_row