import time
from indicators import detect_trend
from futures_api import (
    place_market_order,
    evaluate_position,
    close_position,
    add_position,
    get_position
)

symbols = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT", "ADAUSDT"]
base_qty = {
    "BTCUSDT": 0.001,
    "ETHUSDT": 0.01,
    "SOLUSDT": 0.5,
    "XRPUSDT": 5,
    "ADAUSDT": 5
}

def trade_loop():
    while True:
        for symbol in symbols:
            trend = detect_trend(symbol)
            if not trend:
                print(f"{symbol} 趨勢不一致，跳過")
                continue

            pos = get_position(symbol)
            long_status = evaluate_position(symbol, "LONG")
            short_status = evaluate_position(symbol, "SHORT")

            # --- 建立新倉 ---
            if trend == "up" and (not pos["LONG"] or pos["LONG"]["amt"] == 0):
                print(f"{symbol} 建立 LONG 倉")
                place_market_order(symbol, "BUY", base_qty[symbol], "LONG")

            if trend == "down" and (not pos["SHORT"] or pos["SHORT"]["amt"] == 0):
                print(f"{symbol} 建立 SHORT 倉")
                place_market_order(symbol, "SELL", base_qty[symbol], "SHORT")

            # --- 處理獲利加倉與部分平倉 ---
            if long_status == "take_profit":
                print(f"{symbol} LONG 獲利 >30%，部分平倉並加倉")
                close_position(symbol, "LONG", 0.5)
                add_position(symbol, "LONG", base_qty[symbol])

            if short_status == "take_profit":
                print(f"{symbol} SHORT 獲利 >30%，部分平倉並加倉")
                close_position(symbol, "SHORT", 0.5)
                add_position(symbol, "SHORT", base_qty[symbol])

            # --- 停損邏輯 ---
            if long_status == "stop_loss":
                print(f"{symbol} LONG 回檔止損")
                close_position(symbol, "LONG")

            if short_status == "stop_loss":
                print(f"{symbol} SHORT 回檔止損")
                close_position(symbol, "SHORT")

        time.sleep(60)

if __name__ == "__main__":
    trade_loop()
