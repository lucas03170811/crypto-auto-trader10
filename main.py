import os
import time
from datetime import datetime
from binance.um_futures import UMFutures  # ✅ 正確搭配 1.4.0 版本
from binance.error import ClientError
from trade import manage_position

# 從環境變數中讀取 API Key
API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")

# 初始化 Binance 客戶端
client = UMFutures(key=API_KEY, secret=API_SECRET)

# 監控的幣種清單
SYMBOLS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT", "ADAUSDT"]

# 時間間隔（單位：秒），例如每 60 秒分析一次
INTERVAL = 60

def run_bot():
    print("📈 自動交易機器人啟動中...")
    while True:
        try:
            for symbol in SYMBOLS:
                print(f"\n⏰ 分析幣種: {symbol} | {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")
                signal = analyze_market(client, symbol)
                if signal:
                    manage_position(client, symbol, signal)
                else:
                    print(f"🔍 無交易訊號: {symbol}")

        except Exception as e:
            print(f"⚠️ 發生錯誤: {e}")

        time.sleep(INTERVAL)

if __name__ == "__main__":
    run_bot()
