import os
import time
from datetime import datetime
from binance.um_futures import UMFutures
from strategy import analyze_market
from trade import manage_position

API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")

client = UMFutures(key=API_KEY, secret=API_SECRET)

symbols = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT", "ADAUSDT"]
intervals = ["15m", "1h"]

def run():
    while True:
        print(f"===== {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} =====")
        for symbol in symbols:
            try:
                signal = analyze_market(client, symbol, intervals)
                if signal:
                    manage_position(client, symbol, signal)
            except Exception as e:
                print(f"[ERROR] {symbol}: {e}")
        time.sleep(60)

if __name__ == "__main__":
    run()
