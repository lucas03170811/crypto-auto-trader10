import time
from futures_api import check_and_trade
from utils import log_message

SYMBOLS = ["BTCUSDT", "ETHUSDT", "SOLUSDT"]

if __name__ == "__main__":
    log_message("📈 合約自動交易機器人已啟動（每分鐘分析 + RSI + VOL + 止損）")
    while True:
        for symbol in SYMBOLS:
            try:
                check_and_trade(symbol)
            except Exception as e:
                log_message(f"❌ {symbol} 發生錯誤: {e}")
        time.sleep(60)