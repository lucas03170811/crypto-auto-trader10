import requests

def get_signal(symbol):
    klines = get_klines(symbol, interval='15m', limit=50)
    closes = [float(k[4]) for k in klines]
    volume = [float(k[5]) for k in klines]

    # 計算簡單 RSI
    rsi = compute_rsi(closes)
    vol_avg = sum(volume[-10:]) / 10

    if rsi < 30 and volume[-1] > vol_avg:
        return 'BUY'
    elif rsi > 70 and volume[-1] > vol_avg:
        return 'SELL'
    else:
        return 'HOLD'

def get_klines(symbol, interval='1h', limit=100):
    url = f"https://fapi.binance.com/fapi/v1/klines?symbol={symbol}&interval={interval}&limit={limit}"
    response = requests.get(url)
    return response.json()

def compute_rsi(data, period=14):
    gain = 0
    loss = 0
    for i in range(1, period+1):
        delta = data[-i] - data[-i-1]
        if delta > 0:
            gain += delta
        else:
            loss -= delta
    if loss == 0:
        return 100
    rs = gain / loss
    return 100 - (100 / (1 + rs))
