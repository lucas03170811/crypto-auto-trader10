import ta
import pandas as pd
from binance_client import get_klines

def get_indicators(symbol):
    df_15m = get_klines(symbol, interval="15m", limit=100)
    df_1h = get_klines(symbol, interval="1h", limit=100)

    def apply_ta(df):
        df["rsi"] = ta.momentum.RSIIndicator(df["close"]).rsi()
        df["ema_fast"] = ta.trend.EMAIndicator(df["close"], window=9).ema_indicator()
        df["ema_slow"] = ta.trend.EMAIndicator(df["close"], window=21).ema_indicator()
        df["macd"] = ta.trend.MACD(df["close"]).macd_diff()
        df["boll_up"], df["boll_mid"], df["boll_low"] = ta.volatility.BollingerBands(df["close"]).bollinger_hband(), ta.volatility.BollingerBands(df["close"]).bollinger_mavg(), ta.volatility.BollingerBands(df["close"]).bollinger_lband()
        df["volume_growth"] = df["volume"].pct_change()
        return df

    df_15m = apply_ta(df_15m)
    df_1h = apply_ta(df_1h)

    last_rsi = df_15m["rsi"].iloc[-1]
    trend = "LONG" if df_1h["ema_fast"].iloc[-1] > df_1h["ema_slow"].iloc[-1] else "SHORT"
    vol_growth = df_15m["volume_growth"].iloc[-1] > 0.2
    macd_positive = df_1h["macd"].iloc[-1] > 0

    should_open = last_rsi > 50 and macd_positive and vol_growth

    return {
        "rsi": round(last_rsi, 2),
        "ema_trend": trend,
        "vol_growth": vol_growth,
        "trend": trend,
        "should_open": should_open
    }
