import time

positions = {}

def manage_position(client, symbol, signal):
    position_info = client.get_position_risk(symbol=symbol)
    pos = next((p for p in position_info if float(p["positionAmt"]) != 0), None)
    amt = abs(float(pos["positionAmt"])) if pos else 0
    entry = float(pos["entryPrice"]) if pos else 0
    side = "LONG" if float(pos["positionAmt"]) > 0 else "SHORT" if float(pos["positionAmt"]) < 0 else None
    mark_price = float(client.ticker_price(symbol)["price"])

    # 無倉位 → 開倉
    if not pos:
        order_side = "BUY" if signal == "buy" else "SELL"
        qty = round(10 / mark_price, 3)
        client.new_order(symbol=symbol, side=order_side, type="MARKET", quantity=qty)
        print(f"【開倉】{symbol} → {order_side} {qty}")
        positions[symbol] = {
            "entry": mark_price,
            "qty": qty,
            "side": order_side,
            "trail": mark_price,
            "profit_pct": 0
        }
        return

    # 同方向 → 加倉 或 滾倉策略
    if (signal == "buy" and side == "LONG") or (signal == "sell" and side == "SHORT"):
        change_pct = (mark_price - entry) / entry * 100 if side == "LONG" else (entry - mark_price) / entry * 100
        positions[symbol]["profit_pct"] = change_pct

        # 利潤 > 30% → 加倉
        if change_pct > 30:
            qty = round(5 / mark_price, 3)
            order_side = "BUY" if side == "LONG" else "SELL"
            client.new_order(symbol=symbol, side=order_side, type="MARKET", quantity=qty)
            print(f"【加倉】{symbol} → {order_side} {qty}")

        # 利潤 > 50% → 平倉 50%
        if change_pct > 50:
            qty = round(amt / 2, 3)
            order_side = "SELL" if side == "LONG" else "BUY"
            client.new_order(symbol=symbol, side=order_side, type="MARKET", quantity=qty)
            print(f"【平倉一半】{symbol} → {order_side} {qty}")

        # 回調 15% → 全部平倉
        peak = positions[symbol]["trail"]
        retrace = (peak - mark_price) / peak * 100 if side == "LONG" else (mark_price - peak) / peak * 100
        if change_pct > 30 and retrace > 15:
            qty = round(amt, 3)
            order_side = "SELL" if side == "LONG" else "BUY"
            client.new_order(symbol=symbol, side=order_side, type="MARKET", quantity=qty)
            print(f"【止盈止損】{symbol} → {order_side} {qty}")
            positions.pop(symbol)
        else:
            positions[symbol]["trail"] = max(peak, mark_price) if side == "LONG" else min(peak, mark_price)
        return

    # 反向訊號 → 全部平倉
    qty = round(amt, 3)
    order_side = "SELL" if side == "LONG" else "BUY"
    client.new_order(symbol=symbol, side=order_side, type="MARKET", quantity=qty)
    print(f"【反向平倉】{symbol} → {order_side} {qty}")
    positions.pop(symbol)
