import csv
import pandas as pd


class Position:
    def __init__(self):
        self.founds = 50
        self.coin_traded = 0
        self.traded = 0
        self.gained = 0
        self.max_trade = 20
        self.last_price = 0

    def is_traded(self):
        return self.traded >= self.max_trade

    def print_table(self, last_price: float):
        print(f"{'Founds':<10}{'Traded':<10}{'Gained':<10}{
            'Max Trade':<10}{'Coin Traded':<10}{'COIN-USDT':<10}")
        print(f"{self.founds:<10.2f}{self.traded:<10.2f}{self.gained:<10.2f}{
            self.max_trade:<10.2f}{self.coin_traded:<10.2e}{self.coin_traded*last_price:<10.2f}")
    
    def re_buy(self, last_price):
        self.execute_sell_trade(last_price)
        self.execute_buy_trade(last_price)
    
    def execute_buy_trade(self, current_price: float):
        self.founds -= self.max_trade
        self.coin_traded += self.max_trade / current_price
        self.traded += self.max_trade
    
    def execute_sell_trade(self, current_price: float):
        sell = self.coin_traded * current_price
        self.founds += sell
        self.coin_traded = 0
        self.traded = 0
        self.gained += sell - self.max_trade

    def buy(self, last_price: float):

        if (self.is_traded()):
            return

        self.execute_buy_trade(last_price)
    
    def sell(self, last_price: float):
        if(self.coin_traded == 0):
            return

        self.execute_sell_trade(last_price)

class KeeperPosition(Position):
    def __init__(self, delta: float):
        self.delta = delta
        super().__init__()
    
    def buy(self, last_price: float):

        previous_price = self.last_price
        current_price = last_price
        price_change_ratio = self.delta

        rebuy_condition = previous_price != 0 and current_price * price_change_ratio > previous_price
        if (self.is_traded() and rebuy_condition):
            self.re_buy(last_price)
            return

        if (self.is_traded()):
            return

        self.execute_buy_trade(current_price)
    
    def sell(self, last_price: float):
        if(self.coin_traded == 0):
            return

        self.execute_sell_trade(last_price)
