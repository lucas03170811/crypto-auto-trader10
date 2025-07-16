import os
from binance.client import Client
from indicators import get_rsi, get_volatility
from utils import log_message, stop_loss_triggered

api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_API_SECRET")
client = Client(api_key, api_secret)
positions = {}

def check_and_trade(symbol):
    candles = client.futures_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1MINUTE, limit=100)
    closes = [float(c[4]) for c in candles]
    volumes = [float(c[5]) for c in candles]
    price = closes[-1]
    rsi = get_rsi(closes)
    vol_ok = get_volatility(volumes)
    log_message(f"[{symbol}] 價格: {price:.2f} | RSI: {rsi:.2f} | VOL增長: {vol_ok}")

    holding = positions.get(symbol)
    action = None

    if holding:
        entry = holding["entry"]
        if stop_loss_triggered(entry, price, 0.2):
            action = "close"
        elif rsi > 70:
            action = "close"
    else:
        if rsi < 30 and vol_ok:
            action = "long"

    qty = 0.01  # 固定下單數量（可視資金修改）

    if action == "long":
        client.futures_create_order(symbol=symbol, side="BUY", type="MARKET", quantity=qty)
        positions[symbol] = {"entry": price}
        log_message(f"✅ 開多 {symbol} @ {price:.2f}")

    elif action == "close":
        client.futures_create_order(symbol=symbol, side="SELL", type="MARKET", quantity=qty)
        positions.pop(symbol, None)
        log_message(f"✅ 平倉 {symbol} @ {price:.2f}")