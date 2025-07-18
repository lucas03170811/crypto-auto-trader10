import numpy as np
import pandas as pd
from indicators import calculate_indicators

def analyze_market(client, symbol, intervals):
    signals = []
    for interval in intervals:
        klines = client.klines(symbol=symbol, interval=interval, limit=100)
        df = pd.DataFrame(klines, columns=[
            'time', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_asset_volume', 'trades',
            'taker_base_volume', 'taker_quote_volume', 'ignore'
        ])
        df["close"] = pd.to_numeric(df["close"])
        df["volume"] = pd.to_numeric(df["volume"])
        df = calculate_indicators(df)

        if df["signal"].iloc[-1] != "":
            signals.append(df["signal"].iloc[-1])
    if len(signals) == len(intervals) and all(s == signals[0] for s in signals):
        return signals[0]
    return ""
