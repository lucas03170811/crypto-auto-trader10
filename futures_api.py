import os
from binance.um_futures import UMFutures
from binance.error import ClientError
from indicators import get_signal
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_API_SECRET")
client = UMFutures(api_key=api_key, api_secret=api_secret)

symbols = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT", "ADAUSDT"]
quantity_usdt = 20

position_status = {}

for symbol in symbols:
    position_status[symbol] = {
        "side": None,
        "entry_price": 0.0,
        "last_price": 0.0
    }

def check_and_trade():
    for symbol in symbols:
        try:
            signal = get_signal(symbol)
            print(f"{symbol} signal: {signal}")

            position = client.get_position_risk(symbol=symbol)
            qty = float(position[0]['positionAmt'])
            entry_price = float(position[0]['entryPrice'])
            mark_price = float(position[0]['markPrice'])

            profit_rate = ((mark_price - entry_price) / entry_price) * 100 if qty != 0 else 0

            if signal == 'BUY' and qty == 0:
                client.new_order(symbol=symbol, side="BUY", type="MARKET", quantity=calc_qty(symbol))
                position_status[symbol] = {"side": "LONG", "entry_price": mark_price, "last_price": mark_price}

            elif signal == 'SELL' and qty == 0:
                client.new_order(symbol=symbol, side="SELL", type="MARKET", quantity=calc_qty(symbol))
                position_status[symbol] = {"side": "SHORT", "entry_price": mark_price, "last_price": mark_price}

            elif qty != 0:
                if (position_status[symbol]['side'] == 'LONG' and profit_rate <= -15) or \
                   (position_status[symbol]['side'] == 'SHORT' and profit_rate <= -15):
                    close_position(symbol, qty)

                elif (position_status[symbol]['side'] == 'LONG' and profit_rate >= 30):
                    # 加倉
                    client.new_order(symbol=symbol, side="BUY", type="MARKET", quantity=calc_qty(symbol))
                    if profit_rate >= 50:
                        close_position(symbol, qty / 2)  # 平倉一半

                elif (position_status[symbol]['side'] == 'SHORT' and profit_rate >= 30):
                    client.new_order(symbol=symbol, side="SELL", type="MARKET", quantity=calc_qty(symbol))
                    if profit_rate >= 50:
                        close_position(symbol, qty / 2)

        except ClientError as ce:
            print(f"Binance Client error: {ce}")
        except Exception as e:
            print(f"Error while processing {symbol}: {e}")

def calc_qty(symbol):
    price = float(client.ticker_price(symbol=symbol)['price'])
    qty = round(quantity_usdt / price, 3)
    return qty

def close_position(symbol, qty):
    side = "SELL" if qty > 0 else "BUY"
    client.new_order(symbol=symbol, side=side, type="MARKET", quantity=abs(qty))
    position_status[symbol] = {"side": None, "entry_price": 0.0, "last_price": 0.0}
