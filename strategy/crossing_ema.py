import pandas as pd

from analyse import transform
from .base import BaseStrategy, StrategyVariables, get_ticker_last_data

class CrossingVariables(StrategyVariables):
    def __init__(self, last_datetime:float, last_price: float, short_last_ema: float, long_last_ema: float):
        self.last_datetime = last_datetime
        self.last_price = last_price
        self.short_last_ema = short_last_ema
        self.long_last_ema = long_last_ema 
    
    def print(self)->None:
        print(f"{'datetime':<15}{'Last Price':<15}{'Last EMA':<15}")
        print(f"{self.last_datetime:<15.2f}{self.last_price:<15.2f}{self.last_ema:<15.2f}")

def calculate_indicators(data: pd.DataFrame, short=50, long=100)->float:
    short_id = transform.ema_id(short)
    transform.insert_ema(data, short)
    short_last_ema = data[short_id].iloc[-1]

    long_id = transform.ema_id(long)
    transform.insert_ema(data, long)
    long_last_ema = data[long_id].iloc[-1]

    return short_last_ema, long_last_ema
    
def buy_ema_condtion(variables: CrossingVariables)->bool:
    return variables.short_last_ema > variables.long_last_ema

class Strategy(BaseStrategy):
    def __init__(self, ticker_name: str, position, short: int, long: int, verbose=False):
        self.ticker_name = ticker_name
        self.position = position
        self.verbose = verbose
        self.short = short
        self.long = long
    
    def execute(self, ticker_data: pd.DataFrame)->CrossingVariables:
        last_price, last_datetime = get_ticker_last_data(ticker_data)
        short_last_ema, long_last_ema = calculate_indicators(ticker_data, self.short, self.long)

        variables = CrossingVariables(last_datetime, last_price, short_last_ema, long_last_ema)

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
            "last_short_ema": variables.short_last_ema,
            "last_long_ema": variables.long_last_ema
        }
        data.loc[len(data)] = new_row