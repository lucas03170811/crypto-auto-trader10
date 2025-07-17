from futures_api import check_and_trade
import time

if __name__ == '__main__':
    while True:
        try:
            check_and_trade()
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(60)

        time.sleep(60)

if __name__ == "__main__":
    trade_loop()
