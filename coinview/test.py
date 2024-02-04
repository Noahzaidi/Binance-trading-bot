import config
import numpy 
import talib
from numpy import genfromtxt

from binance import Client

client =Client(config.API_KEY,config.API_SECRET)

prices = client.get_all_tickers()


for price in prices:
    print(price)


# candles = client.get_klines(symbol="BTCUSDT", interval=Client.KLINE_INTERVAL_5MINUTE)

# print(len(candles))

# for candlestick in candles:
#     print(candlestick)



# close=numpy.random.random(100)

# (print(close))

# moving_average=(talib.SMA(close, timeperiod=10))

# print(moving_average)


# myData=genfromtxt("2023_15minutes.csv",delimiter =",")

# print(myData)