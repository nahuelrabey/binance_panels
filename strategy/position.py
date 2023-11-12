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