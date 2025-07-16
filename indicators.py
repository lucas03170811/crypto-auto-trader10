import numpy as np

def get_rsi(closes, period=14):
    deltas = np.diff(closes)
    gains = np.where(deltas > 0, deltas, 0)
    losses = np.where(deltas < 0, -deltas, 0)
    avg_gain = np.mean(gains[-period:])
    avg_loss = np.mean(losses[-period:])
    rs = avg_gain / avg_loss if avg_loss != 0 else 0
    return 100 - (100 / (1 + rs))

def get_volatility(volumes, threshold=1.3):
    recent = np.mean(volumes[-3:])
    past = np.mean(volumes[-10:-3])
    return recent > past * threshold