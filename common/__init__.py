import signal
import logging
def time_out(interval):
    def decorator(func):
        def handler(signum, frame):
            raise TimeoutError
        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(interval)
            result = func(*args, **kwargs)
            signal.alarm(0)
            return result
        return wrapper
    return decorator
