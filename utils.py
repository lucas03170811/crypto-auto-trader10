def log_message(msg):
    from datetime import datetime
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{now}] {msg}")

def stop_loss_triggered(entry_price, current_price, max_loss=0.2):
    return (current_price - entry_price) / entry_price <= -max_loss