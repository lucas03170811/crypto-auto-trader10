import pandas as pd
from binance.um_futures import UMFutures

client = UMFutures()

def get_klines(symbol: str, interval: str, limit: int = 100):
    data = client.klines(symbol=symbol, interval=interval, limit=limit)
    df = pd.DataFrame(data, columns=[
        "timestamp", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "number_of_trades",
        "taker_buy_base", "taker_buy_quote", "ignore"
    ])
    df["close"] = pd.to_numeric(df["close"])
    df["open"] = pd.to_numeric(df["open"])
    return df
