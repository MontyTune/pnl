# pnl
Each trade consists of the time it happened, a symbol, whether you bought or sold,
price, and quantity traded.

Calculates the PnL using FIFO matching.

Can either print all trades made and PnL directly, or also store trades made.

Ex:

TIME,SYMBOL,SIDE,PRICE,QUANTITY
2,AAPL,B,32.58,300
2,GOOG,S,1100.48,200
7,AAPL,S,40.07,3000
10,GOOG,S,1087.07,300
12,GOOG,B,1034.48,500 

becomes

OPEN_TIME,CLOSE_TIME,SYMBOL,QUANTITY,PNL,OPEN_SIDE,CLOSE_SIDE,OPEN_PRICE,CLOSE_PRICE
2,7,AAPL,300,2247.00,B,S,32.58,40.07
2,12,GOOG,200,13200.00,S,B,1100.48,1034.48
10,12,GOOG,300,15777.00,S,B,1087.07,1034.48
31224.00
