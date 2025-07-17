def detect_trend(klines_15m, klines_1h):
    def calculate_ema(prices, period=20):
        ema = []
        k = 2 / (period + 1)
        for i in range(len(prices)):
            if i < period:
                ema.append(None)
            elif i == period:
                ema.append(sum(prices[:period]) / period)
            else:
                ema.append(prices[i] * k + ema[-1] * (1 - k))
        return ema

    def calculate_rsi(prices, period=14):
        deltas = [prices[i] - prices[i - 1] for i in range(1, len(prices))]
        gains = [delta if delta > 0 else 0 for delta in deltas]
        losses = [-delta if delta < 0 else 0 for delta in deltas]
        avg_gain = sum(gains[:period]) / period
        avg_loss = sum(losses[:period]) / period
        rsi = []
        for i in range(period, len(prices)):
            gain = gains[i - 1]
            loss = losses[i - 1]
            avg_gain = (avg_gain * (period - 1) + gain) / period
            avg_loss = (avg_loss * (period - 1) + loss) / period
            if avg_loss == 0:
                rsi.append(100)
            else:
                rs = avg_gain / avg_loss
                rsi.append(100 - (100 / (1 + rs)))
        return [None] * (period) + rsi

    def analyze_trend(klines):
        close_prices = [float(k[4]) for k in klines]
        ema = calculate_ema(close_prices)
        rsi = calculate_rsi(close_prices)

        if ema[-1] and close_prices[-1] > ema[-1] and rsi[-1] > 55:
            return "bullish"
        elif ema[-1] and close_prices[-1] < ema[-1] and rsi[-1] < 45:
            return "bearish"
        else:
            return "neutral"

    trend_15m = analyze_trend(klines_15m)
    trend_1h = analyze_trend(klines_1h)

    if trend_15m == trend_1h:
        return trend_15m
    else:
        return "neutral"
