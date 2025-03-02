import time
import functools

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
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        print(f"function '{func.__name__}' took {end_time - start_time:.6f} seconds.")
        return result
    return wrapper
