#! python3

import ping3
import requests
import time


def get_timestamp():
    return time.strftime("%d/%m %H:%M", time.localtime())

def get_response_time(url = None):
    if not url:
        url = 'google.com'

    try:
        timestamp = get_timestamp()
        start_time = time.time()
        response = ping3.ping(url, timeout=30)
        # response = requests.get(url, timeout=30)
        end_time = time.time()

        if response is not None:
            elapsed_time = round(end_time - start_time, 1)
            print(f"{timestamp} PING OK {elapsed_time} seg")
        else:
            print(f"{timestamp} PING FAILED")

    except requests.RequestException as e:
        print(f"{timestamp} PING FAILED: {e}")

if __name__ == "__main__":

    get_response_time()
