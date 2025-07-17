from binance.um_futures import UMFutures
from binance.error import ClientError
from utils import current_time
import math

client = UMFutures()

# 下市價單
def place_market_order(symbol, side, quantity, position_side):
    try:
        order = client.new_order(
            symbol=symbol,
            side=side,
            type="MARKET",
            quantity=quantity,
            positionSide=position_side
        )
        print(f"[{current_time()}] 訂單成功: {order}")
        return order
    except ClientError as e:
        print(f"[{current_time()}] 下單錯誤: {e}")
        return None

# 查詢目前持倉
def get_position(symbol):
    positions = client.position_information(symbol=symbol)
    pos_data = {"LONG": None, "SHORT": None}
    for pos in positions:
        side = "LONG" if pos["positionSide"] == "LONG" else "SHORT"
        pos_data[side] = {
            "amt": float(pos["positionAmt"]),
            "entry_price": float(pos["entryPrice"]),
            "unrealized_profit": float(pos["unRealizedProfit"]),
        }
    return pos_data

# 判斷是否可以加倉或平倉
def evaluate_position(symbol, position_side, percent_trigger=30, retrace_trigger=15):
    pos = get_position(symbol).get(position_side.upper())
    if not pos or pos["amt"] == 0:
        return "none"

    entry = pos["entry_price"]
    amt = abs(pos["amt"])
    profit = pos["unrealized_profit"]
    current_price = float(client.ticker_price(symbol=symbol)["price"])
    change_percent = ((current_price - entry) / entry * 100) if position_side == "LONG" else ((entry - current_price) / entry * 100)

    print(f"[{current_time()}] {symbol}-{position_side} 獲利率: {change_percent:.2f}%")

    if change_percent >= percent_trigger:
        return "take_profit"  # 觸發獲利加倉
    elif change_percent <= -retrace_trigger:
        return "stop_loss"  # 回檔止損
    return "hold"

# 平倉（部分或全部）
def close_position(symbol, position_side, ratio=1.0):
    pos = get_position(symbol).get(position_side.upper())
    if pos and pos["amt"] != 0:
        qty = abs(pos["amt"]) * ratio
        side = "SELL" if position_side == "LONG" else "BUY"
        place_market_order(symbol, side, round(qty, 3), position_side)

# 加倉
def add_position(symbol, position_side, base_qty):
    side = "BUY" if position_side == "LONG" else "SELL"
    place_market_order(symbol, side, base_qty, position_side)
