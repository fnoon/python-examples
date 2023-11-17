# An example use of Python decorators.
# Based upon https://youtu.be/-MHrG5Ep6yg?si=HyRb4FutdWe61Oee

from functools import wraps
from time import perf_counter, sleep


def get_time(func):
    """Times any function"""

    @wraps(func)   # so that caller can get 'func's properties, not wrapper()'s
    def wrapper(*args, **kwargs):
        """This function will take 'func's arguments"""
        print(args, kwargs)
        start_time = perf_counter()
        func(*args, *kwargs)
        end_time = perf_counter()
        time_spent = round(end_time - start_time, 2)
        print('Time', time_spent, 'seconds')

    return wrapper


@get_time
def do_something(param: str):
    """Does something important"""

    sleep(1)
    print(param)


if __name__ == '__main__':
    do_something('Hello')

    # does the "right thing" because of above "@wraps()":
    print(do_something.__name__)

   # ditto:
    print(do_something.__doc__)
