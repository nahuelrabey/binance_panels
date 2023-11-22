from . import Position
from ABC import ABSMeta

class Ringer(metaclass=ABSMeta):
    def buy():
        pass
    def sell():
        pass
    
class RingPosition(Position):
    def __init__(self, ringer: Ringer):
        self.ringer = ringer
        super().__init__()
    
    def buy(self, last_price: float):
        self.ringer.buy()
    
    def sell(self, last_price: float):
        self.ringer.sell()
    
    