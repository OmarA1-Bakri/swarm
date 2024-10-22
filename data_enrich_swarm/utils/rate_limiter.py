# rate_limiter.py

import time
from threading import Lock
import logging


class RateLimiter:
    def __init__(self, max_calls_per_minute):
        self.max_calls = max_calls_per_minute
        self.calls = []
        self.lock = Lock()

    def __enter__(self):
        with self.lock:
            now = time.time()
            self.calls = [t for t in self.calls if now - t < 60]
            if len(self.calls) >= self.max_calls:
                sleep_time = 60 - (now - self.calls[0])
                try:
                    time.sleep(sleep_time)
                except Exception as e:
                    logging.error(f"Error during sleep in rate limiter: {e}")
                    raise RuntimeError(f"Error during sleep in rate limiter: {e}")
            self.calls.append(time.time())

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
