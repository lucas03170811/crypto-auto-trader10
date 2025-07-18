from indicators import get_indicators
from binance_client import client, open_position, close_position, get_position, get_balance
import traceback

SYMBOLS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT", "ADAUSDT"]

def analyze_and_trade():
    for symbol in SYMBOLS:
        try:
            indicators = get_indicators(symbol)
            print(f"[{symbol}] RSI: {indicators['rsi']} | EMA Trend: {indicators['ema_trend']} | VOL: {indicators['vol_growth']}")

            position = get_position(symbol)

            if position:
                entry_price = float(position["entryPrice"])
                mark_price = float(position["markPrice"])
                profit_pct = (mark_price - entry_price) / entry_price * 100 if position["positionAmt"] != "0" else 0

                if profit_pct >= 30:
                    print(f"💰 {symbol} 獲利 {profit_pct:.2f}%，執行部分平倉並加倉")
                    close_position(symbol, portion=0.5)
                    open_position(symbol, side=position["positionSide"], size_pct=50)

                elif profit_pct <= -20:
                    print(f"⚠️ {symbol} 已達止損，平倉")
                    close_position(symbol)
            else:
                if indicators["should_open"]:
                    side = indicators["trend"]
                    print(f"🚀 {symbol} 判斷開倉方向：{side}")
                    open_position(symbol, side)

        except Exception as e:
            print(f"❌ {symbol} 發生錯誤: {e}")
            traceback.print_exc()
