# rate_limiter.py

import time
from threading import Lock


class RateLimiter:
    """
    A simple rate limiter to control the number of API calls made within a minute.

    Attributes:
        max_calls (int): Maximum number of calls allowed per minute.
        calls (list): Timestamps of the API calls made.
        lock (Lock): A threading lock to ensure thread-safe operations.
    """

    def __init__(self, max_calls_per_minute):
        """
        Initializes the RateLimiter with a specified maximum number of calls per minute.

        Args:
            max_calls_per_minute (int): The maximum number of API calls allowed per minute.
        """
        self.max_calls = max_calls_per_minute
        self.calls = []
        self.lock = Lock()

    def __enter__(self):
        """
        Enters the rate limiter context, ensuring that the number of calls does not exceed the limit.
        If the limit is reached, it waits until a call can be made.

        Raises:
            RuntimeError: If an error occurs while attempting to sleep.
        """
        with self.lock:
            now = time.time()
            # Remove calls that are older than 60 seconds
            self.calls = [t for t in self.calls if now - t < 60]
            if len(self.calls) >= self.max_calls:
                sleep_time = 60 - (now - self.calls[0])
                try:
                    time.sleep(sleep_time)
                except Exception as e:
                    raise RuntimeError(f"Error during sleep in rate limiter: {e}")
            self.calls.append(time.time())

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exits the rate limiter context. This method is required for the context manager protocol.

        Args:
            exc_type (type): The exception type if an exception was raised, otherwise None.
            exc_val (Exception): The exception instance if an exception was raised, otherwise None.
            exc_tb (traceback): The traceback object if an exception was raised, otherwise None.
        """
        pass
