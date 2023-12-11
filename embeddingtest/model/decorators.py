""" Decorator use for check download time. """
from datetime import datetime

def checktime(func):
    def wrapper(*args, **kwargs):
        start_time = datetime.now()
        result = func(*args, **kwargs)
        end_time = datetime.now()
        print(f"Function call {func.__name__} took {(end_time - start_time).total_seconds()}s to run.")
        return result
    return wrapper