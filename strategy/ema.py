import pandas as pd

from analyse import transform
from .base import BaseStrategy, StrategyVariables, get_ticker_last_data

class EmaVariables(StrategyVariables):
    def __init__(self, last_datetime:float, last_price: float, last_ema: float):
        self.last_datetime = last_datetime
        self.last_price = last_price
        self.last_ema = last_ema
    
    def print(self)->None:
        print(f"{'datetime':<15}{'Last Price':<15}{'Last EMA':<15}")
        print(f"{self.last_datetime:<15.2f}{self.last_price:<15.2f}{self.last_ema:<15.2f}")

def calculate_indicators(data: pd.DataFrame, n=50)->float:
    id = transform.ema_id(n)
    transform.insert_ema(data, n)

    last_ema = data[id].iloc[-1]
    return last_ema
    
def buy_ema_condtion(variables: EmaVariables)->bool:
    return variables.last_price > variables.last_ema

class Strategy(BaseStrategy):
    def __init__(self, ticker_name: str, position, n: int, verbose=False):
        self.ticker_name = ticker_name
        self.position = position
        self.verbose = verbose
        self.n = n
    
    def execute(self, ticker_data: pd.DataFrame)->EmaVariables:
        last_price, last_datetime = get_ticker_last_data(ticker_data)
        last_ema = calculate_indicators(ticker_data, self.n)

        variables = EmaVariables(last_datetime, last_price, last_ema)

        if(buy_ema_condtion(variables)):
            if (self.position.is_traded()):
                return variables
            self.position.buy(last_price)
        
        if(not buy_ema_condtion(variables)):
            if(self.position.coin_traded == 0):
                return variables
            
            self.position.sell(last_price)
        
        return variables
    
    def create_pandas(self) -> pd.DataFrame:
        return pd.DataFrame(columns=["datetime", "founds", "coin_traded", "traded", "gained", "max_trade", "last_price", "last_ema"])
    
    def save_to_pandas(self, variables: StrategyVariables, data: pd.DataFrame):
        new_row = {
            "datetime": variables.last_datetime,
            "founds": self.position.founds,
            "coin_traded": self.position.coin_traded,
            "traded": self.position.traded,
            "gained": self.position.gained,
            "max_trade": self.position.max_trade,
            "last_price": variables.last_price,
            "last_ema": variables.last_ema,
        }
        data.loc[len(data)] = new_row