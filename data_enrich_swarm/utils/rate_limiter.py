# rate_limiter.py

import time
from threading import Lock
import logging


class RateLimiter:
    """
    A simple rate limiter class to control the number of API calls made per minute.

    Attributes:
        max_calls (int): Maximum number of calls allowed per minute.
        calls (list): Timestamps of the calls made.
        lock (Lock): A threading lock to ensure thread safety.
    """

    def __init__(self, max_calls_per_minute):
        """
        Initializes the RateLimiter with a specified maximum number of calls per minute.

        Args:
            max_calls_per_minute (int): The maximum number of calls allowed per minute.
        """
        self.max_calls = (
            max_calls_per_minute  # Set the maximum number of calls allowed per minute
        )
        self.calls = []  # List to store timestamps of calls
        self.lock = Lock()  # Lock to ensure thread safety

    def __enter__(self):
        """
        Enters the rate limiter context, ensuring that the number of calls does not exceed the limit.
        If the limit is reached, it sleeps until a call can be made.

        Returns:
            None
        """
        with self.lock:  # Acquire the lock to ensure thread safety
            now = time.time()  # Get the current time
            # Filter out calls that are older than 60 seconds
            self.calls = [t for t in self.calls if now - t < 60]
            if (
                len(self.calls) >= self.max_calls
            ):  # Check if the number of calls has reached the limit
                sleep_time = 60 - (now - self.calls[0])  # Calculate the time to sleep
                try:
                    time.sleep(sleep_time)  # Sleep until a call can be made
                except Exception as e:
                    logging.error(f"Error during sleep in rate limiter: {e}")
                    raise RuntimeError(f"Error during sleep in rate limiter: {e}")
            self.calls.append(time.time())  # Record the current call time

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exits the rate limiter context. Currently, it does not perform any specific action.

        Args:
            exc_type (type): The exception type if an exception was raised.
            exc_val (Exception): The exception instance if an exception was raised.
            exc_tb (traceback): The traceback object if an exception was raised.

        Returns:
            None
        """
        pass
