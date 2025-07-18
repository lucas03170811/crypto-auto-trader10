import time
import schedule
from trade import analyze_and_trade

def job():
    print("🔍 開始分析市場...")
    analyze_and_trade()

if __name__ == "__main__":
    schedule.every(1).minutes.do(job)
    print("✅ 自動交易系統已啟動，開始執行中...")

    while True:
        schedule.run_pending()
        time.sleep(1)
