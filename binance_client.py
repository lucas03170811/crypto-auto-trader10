from binance.um_futures import UMFutures
import pandas as pd
import os

API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")

client = UMFutures(key=API_KEY, secret=API_SECRET)

def get_klines(symbol, interval="15m", limit=100):
    data = client.klines(symbol, interval=interval, limit=limit)
    df = pd.DataFrame(data, columns=["timestamp", "open", "high", "low", "close", "volume", "", "", "", "", "", ""])
    df["close"] = df["close"].astype(float)
    df["volume"] = df["volume"].astype(float)
    return df

def get_position(symbol):
    positions = client.get_position_risk(symbol=symbol)
    for pos in positions:
        if float(pos["positionAmt"]) != 0:
            return pos
    return None

def open_position(symbol, side="LONG", size_pct=10):
    usdt_balance = float(get_balance())
    qty = round((usdt_balance * size_pct / 100) / float(client.ticker_price(symbol)["price"]), 3)
    side_type = "BUY" if side == "LONG" else "SELL"
    client.new_order(symbol=symbol, side=side_type, type="MARKET", quantity=qty, positionSide=side)

def close_position(symbol, portion=1.0):
    pos = get_position(symbol)
    if pos:
        qty = abs(float(pos["positionAmt"])) * portion
        side_type = "SELL" if float(pos["positionAmt"]) > 0 else "BUY"
        client.new_order(symbol=symbol, side=side_type, type="MARKET", quantity=round(qty, 3), reduceOnly=True)

def get_balance():
    balance = client.balance()
    for b in balance:
        if b["asset"] == "USDT":
            return b["availableBalance"]
