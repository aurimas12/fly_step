import time
import functools
from datetime import datetime, timedelta, timezone


def count_timer(func):
    """
    A decorator that measures and prints the execution time of a function.
    Args:
        func (callable): The function to be timed.
    Returns:
        callable: A wrapped function that prints its execution time.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        """
        Wrapper function that records the execution time of the original function.
        Args:
            *args: Positional arguments passed to the function.
            **kwargs: Keyword arguments passed to the function.
        Returns:
            Any: The return value of the original function.
        """
        start_time = time.monotonic()
        result = func(*args, **kwargs)
        end_time = time.monotonic()
        print(f"function '{func.__name__}' took {end_time - start_time:.6f} seconds.")
        return result
    return wrapper

# TODO:jei dedi tipa koki grazins ar priims dek prie visu funkciju
def get_yesterday_timestamp() -> int:
    """
    Get the Unix timestamp (in milliseconds) for yesterday's date.
    Returns:
        int: Timestamp representing yesterday since the epoch
        1719877200000.
    Example:
        If today is 2025-03-05, the function returns the timestamp for 2025-03-04.
    """
    yesterday = datetime.now(timezone.utc) - timedelta(days=1)
    return int(yesterday.timestamp()) 
