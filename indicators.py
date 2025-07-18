import talib
import numpy as np

def calculate_indicators(df):
    close = df["close"].values
    volume = df["volume"].values

    df["RSI"] = talib.RSI(close, timeperiod=14)
    df["EMA"] = talib.EMA(close, timeperiod=20)
    df["MACD"], _, _ = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
    upper, middle, lower = talib.BBANDS(close, timeperiod=20)
    df["BOLL_UPPER"] = upper
    df["BOLL_LOWER"] = lower

    latest = df.iloc[-1]
    signal = ""
    if latest["close"] > latest["EMA"] and latest["RSI"] > 60 and latest["MACD"] > 0:
        signal = "buy"
    elif latest["close"] < latest["EMA"] and latest["RSI"] < 40 and latest["MACD"] < 0:
        signal = "sell"
    df["signal"] = ""
    df.at[df.index[-1], "signal"] = signal
    return df
