import csv
import sys
from collections import defaultdict, deque

class TradeManager():
    def __init__(self):
        self._open_trades = defaultdict(deque)
        self._closed_trades = []

    def process_trade(self, trade):
        d = self._open_trades[trade.symbol]

        # if no inventory, just add it
        if len(d) == 0:
            d.append(trade)
            return

        # if inventory exists, all trades must be same way (buy or sell)
        # if new trade is same way, again just add it
        if d[0].buying == trade.buying:
            d.append(trade)
            return

        # otherwise, consume the trades
        while len(d) > 0 and trade.quantity > 0:
            quant_traded = min(trade.quantity, d[0].quantity)
            
            pnl = quant_traded * round(trade.price - d[0].price, 2)
            # invert if we shorted
            if trade.buying:
                pnl *= -1

            ct = ClosedTrade(d[0].time, trade.time, trade.symbol,
                    quant_traded, pnl, d[0].buying, d[0].price, trade.price)

            self._closed_trades.append(ct)

            trade.quantity -= quant_traded
            d[0].quantity -= quant_traded
            
            if d[0].quantity == 0:
                d.popleft()

        # if the new trade still has quantity left over
        # then add it
        if trade.quantity > 0:
            d.append(trade)
            
    def print_closed_trades(self):
        print(("OPEN_TIME,CLOSE_TIME,SYMBOL,QUANTITY,PNL,"
                "OPEN_SIDE,CLOSE_SIDE,OPEN_PRICE,CLOSE_PRICE"))
        for ct in self._closed_trades:
            print(ct)

    def get_pnl(self):
        pnl = 0
        for ct in self._closed_trades:
            pnl += ct.pnl

        return pnl

    def get_copy_of_closed_trades(self):
        return self._closed_trades[:]

class Trade():
    def __init__(self, time, symbol, buying, price, quantity):
        self.time = time
        self.symbol = symbol
        self.buying = buying
        self.price = price
        self.quantity = quantity

class ClosedTrade():
    def __init__(self, open_t, close_t, symbol, quantity, pnl, bought_first,
            open_p, close_p):
        self.open_t = open_t
        self.close_t = close_t
        self.symbol = symbol
        self.quantity = quantity
        self.pnl = pnl
        self.bought_first = bought_first
        self.open_p = open_p
        self.close_p = close_p

    def __str__(self):
        s = "{},{},{},{},{:.2f},{},{},{:.2f},{:.2f}"
        s = s.format(
                self.open_t,
                self.close_t,
                self.symbol,
                self.quantity,
                self.pnl,
                "B" if self.bought_first else "S",
                "S" if self.bought_first else "B",
                self.open_p,
                self.close_p
                )
        
        return s

def read_trades(file_name):
    tm = TradeManager()

    with open(file_name, 'r') as trades_csv:
        trade_reader = csv.DictReader(trades_csv, delimiter=',')

        for tr in trade_reader:
            buying = tr["SIDE"] == "B"
            trade = Trade(tr["TIME"], tr["SYMBOL"], buying, 
                    float(tr["PRICE"]), int(tr["QUANTITY"]))
            
            tm.process_trade(trade)
        
        tm.print_closed_trades()
        print("{:.2f}".format(tm.get_pnl()))

if __name__ == "__main__":
    read_trades(sys.argv[1])
