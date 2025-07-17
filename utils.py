import time
from datetime import datetime

def current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def log_message(message):
    timestamp = current_time()
    print(f"[{timestamp}] {message}")
