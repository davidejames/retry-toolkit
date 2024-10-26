# SPDX-FileCopyrightText: © 2024 David E. James
# SPDX-License-Identifier: MIT
# SPDX-FileType: SOURCE
'''A "simple" retry implementation.

Retry has been done and redone many times. Here is a version that takes only
a few arguments that are all optional but provides most of the flexibility
seen in many implementations.

It does not try to define all the different variables that may be used to
compute backoff values, instead preferring to allow a callable that could use
any algorithm desired to compute a backoff of which 3 very simple
implementations are provided. Users can use these as an example to setup their
own perfect backoff implementation (hopefully using jitter as well).

Or perhaps you should not use this module as a dependency, but instead copy
the strategy below, include it in your own codebase, and alter it to make it
your own. MIT is a permissive license.
'''

from collections.abc import Callable
from typing import TypeAlias

import inspect
import time
from functools import wraps


#-------------------------------------------------------------------------------
# Backoff time calculation functions
#-------------------------------------------------------------------------------

def constant(c: float):
    '''Simple constant backoff. Suitable for demonstration.'''
    def _constant(x: float) -> float:
        return c
    return _constant


def linear(m: float, b: float =0):
    '''Linear backoff. Suitable for demonstration.'''
    def _linear(x: float) -> float:
        return m*x + b
    return _linear


def exponential(n: float, b: float = 0):
    '''Exponential backoff. Slightly more realistic.'''
    def _exponential(x: float) -> float:
        return n*(2**x) + b
    return _exponential


#-------------------------------------------------------------------------------
# Private Utilities
#-------------------------------------------------------------------------------

def _ensure_callable(var, default):
    if callable(var):
        return var

    if var is None:
        if callable(default) and not inspect.isclass(default):
            return default

        return lambda *args, **kwargs: default

    return lambda *args, **kwargs: var


#-------------------------------------------------------------------------------
# Defaults for Behaviors:
#-------------------------------------------------------------------------------

class Defaults:
    '''Defaults for retry behavior.

    These values are used if not specified during retry decorator generation
    or if not overriden here (sleep function). For these defaults, it is
    also acceptable to set them to a callable returning the required type
    using the same convention as if it were used as an argument to the
    retry decorator generator.
    '''

    TRIES = 3
    '''integer: How many times to try an operation.'''

    BACKOFF = 0
    '''float: is or returns how long to wait before next retry.'''

    EXC = Exception
    '''
    Defines what exceptions are used for retrying. If any
    exceptions are thrown that do not match this specification then a retry
    will not occur and exception will be raised.
    '''

    SLEEP_FUNC = time.sleep
    '''callable: used as the sleep waiter'''


#-------------------------------------------------------------------------------
# GiveUp - when retry fails:
#-------------------------------------------------------------------------------

class GiveUp(Exception):
    '''Exception class thrown when retries are exhausted.

    Parameters
    ----------
    n_tries    : int
        number of tries attempted

    total_wait : float
        total seconds of wait used

    target_func: callable
        the target function that was attempted (the wrapped function)

    exceptions : list
        list of exceptions for each failed try
    '''

    def __init__(self, n_tries: int, total_wait: float, target_func: callable,
                 exceptions: list):
        self.n_tries     = n_tries
        self.total_wait  = total_wait
        self.target_func = target_func
        self.exceptions  = exceptions


#-------------------------------------------------------------------------------
# Retry Function:
#-------------------------------------------------------------------------------

# The Exception types are particularly messy, some aliases may make it easier
# to understand...
ExceptionTuple: TypeAlias = tuple[type(Exception),...]
ExceptionFunc : TypeAlias = Callable[[],ExceptionTuple|type(Exception)]

def retry(
    tries      : int | Callable[[],int] = None,
    backoff    : int | Callable[[int],int] = None,
    exceptions : type(Exception) | ExceptionTuple | ExceptionFunc = None
    ):
    '''Decorator factory, enables retries.

    This is a decorator factory with some arguments to customize the retry
    behavior. Either specify constants or callables that will return the
    appropriate constants.

    The parameters can also be set to callables returning the type indicated
    below. For backoff, the callable must be able to take a single argument
    which will be the retry number (1 for first retry, 2 for second, etc).

    Parameters
    ----------
    tries:
        Number of times to try an operation including the first attempt which
        is not technically a RE-try.

        If set to a callable, it must have signature:

            () -> int

        If not present in arguments, Defaults.TRIES is used.

    backoff:
        Value in seconds of an amount to wait before next attempt. Can also
        be set to a callable taking the number of retries that must return
        the time to wait.

        If set to a callable, it must have signature:

            (int) -> float

        If not present in arguments, Defaults.BACKOFF is used.

    exceptions:
        Defines the exceptions to to catch for retrying. Exceptions thrown that
        are not caught will bypass further retries, be raised normally, and
        not result in a GiveUp being thrown.

        if set to a callable, it must have signature:

            () -> tuple[Exception,...] | Exception

        If not present in arguments, Defaults.EXC is used.

    Returns
    -------
    : *
        This decorator factory returns a decorator used to wrap a function. The
        wrapped function will have retry behavior and when called it will return
        whatever it normally would.

    Raises
    ------
    GiveUp
        Thrown when retries are exhausted.
    '''

    def _retry_decorator(func):
        @wraps(func)
        def _retry_wrapper(*args, **kwargs):
            # configure at call-time to allow any changes to defaults
            # to properly take effect each time func is used
            n_tries_f = _ensure_callable(tries      , Defaults.TRIES  )
            backoff_f = _ensure_callable(backoff    , Defaults.BACKOFF)
            exc_f     = _ensure_callable(exceptions , Defaults.EXC    )
            sleep_f   = Defaults.SLEEP_FUNC

            n_tries = n_tries_f()
            exc     = exc_f()

            # context/state
            total_sleep    = 0.0
            exception_list = []

            for try_num in range(n_tries):

                if try_num > 0:
                    sleep_time = backoff_f(try_num-1)
                    total_sleep += sleep_time
                    sleep_f(sleep_time)

                try:
                    return func(*args, **kwargs)
                except exc as e:
                    exception_list.append(e)

            raise GiveUp(try_num+1, total_sleep, func, exception_list)

        return _retry_wrapper
    return _retry_decorator


