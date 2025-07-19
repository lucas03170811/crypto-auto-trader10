import os
import time
from datetime import datetime
from binance.um_futures import UMFutures
from binance.error import ClientError
from strategy import analyze_market     # ✅ 補上這行
from trade import manage_position

# 從環境變數中讀取 API Key
API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")

# 檢查是否有設定 API 金鑰
if not API_KEY or not API_SECRET:
    raise ValueError("請確認已正確設置環境變數 BINANCE_API_KEY 與 BINANCE_API_SECRET")

# 初始化 Binance 客戶端
client = UMFutures(key=API_KEY, secret=API_SECRET)

# 監控的幣種清單
SYMBOLS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT", "ADAUSDT"]

# 時間間隔（單位：秒）
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
