
import time
from functools import wraps

# Backoff time calculation functions
def exponential(n, b=0):
    def _exponential(x):
        return n*(2**x) + b
    return _exponential


def linear(m, b=0):
    def _linear(x):
        return m*x + b
    return _linear


def _ensure_callable(var, default):
    if callable(var):
        return var

    if var is None:
        return lambda *args, **kwargs: default

    return lambda *args, **kwargs: var


DEFAULT_TRIES   = 3
DEFAULT_BACKOFF = 0
DEFAULT_EXC     = Exception
SLEEP_FUNC      = time.sleep

class GiveUp(Exception):
    pass


def retry(tries=None, backoff=None, exceptions=None):
    '''

    '''
    tries_f   = _ensure_callable(tries      , DEFAULT_TRIES  )
    backoff_f = _ensure_callable(backoff    , DEFAULT_BACKOFF)
    exc_f     = _ensure_callable(exceptions , DEFAULT_EXC    )
    sleep_f   = SLEEP_FUNC

    def _retry_wrapper(func):
        @wraps(func)
        def _retry(*args, **kwargs):
            n_tries = tries_f()
            exc     = exc_f()

            for try_num in range(n_tries):

                if try_num > 0:
                    sleep_f(backoff_f(try_num-1))

                try:
                    return func(*args, **kwargs)
                except exc as e:
                    pass

            raise GiveUp()

        return _retry
    return _retry_wrapper


