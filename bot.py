import ccxt
import pandas as pd
import requests
import time
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": msg}
    requests.post(url,data=data)

exchange = ccxt.binance()

symbol = "BTC/USDT"
timeframe = "5m"

while True:

    ohlcv = exchange.fetch_ohlcv(symbol,timeframe,limit=100)

    df = pd.DataFrame(ohlcv,columns=["time","open","high","low","close","volume"])

    df["EMA20"] = df["close"].ewm(span=20).mean()
    df["EMA50"] = df["close"].ewm(span=50).mean()

    last = df.iloc[-1]

    price = last["close"]

    if last["EMA20"] > last["EMA50"]:
        send_telegram(f"BUY SIGNAL {symbol}\nPrice: {price}")

    if last["EMA20"] < last["EMA50"]:
        send_telegram(f"SELL SIGNAL {symbol}\nPrice: {price}")

    time.sleep(300)
