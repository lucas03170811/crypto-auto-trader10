mport time
from datetime import datetime

def get_timestamp():
    return int(time.time() * 1000)

def current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
