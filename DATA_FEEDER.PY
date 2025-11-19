import ccxt
import pandas as pd
from datetime import datetime, timedelta

# configuration
exchange = ccxt.binance()
symbol = 'BTC/USDT'
timeframe = '15m' # available time frames '1s', '1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d', '1w', '1M'
since = exchange.parse8601((datetime.utcnow() - timedelta(days=365*2)).strftime('%Y-%m-%dT%H:%M:%S'))  # 2 years back
limit = 1000  # max candles per one query (do not exceed 1000 candles at a time)

all_candles = []
while True:
    candles = exchange.fetch_ohlcv(symbol, timeframe=timeframe, since=since, limit=limit)
    if not candles:
        break
    all_candles.extend(candles)
    since = candles[-1][0] + 1  # next starting point (ms)

    # stop, if we reached now
    if since >= exchange.milliseconds():
        break

# conversion to DataFrame
df = pd.DataFrame(all_candles, columns=['Open time', 'Open', 'High', 'Low', 'Close', 'Volume'])

# date formatting
df['Open time'] = pd.to_datetime(df['Open time'], unit='ms')

# save to CSV
df.to_csv('BTCUSDT_1h.csv', index=False)
print("Fetched candles:", len(df))
print(df.head(10))
