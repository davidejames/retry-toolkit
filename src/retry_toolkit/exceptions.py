#┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅#
# SPDX-FileCopyrightText: © 2024 David E. James
# SPDX-License-Identifier: MIT
# SPDX-FileType: SOURCE
#┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈#

from collections.abc import Callable
from typing import TypeAlias


# The Exception types are particularly messy, some aliases may make it easier
# to understand...
ExceptionTuple: TypeAlias = tuple[type(Exception),...]
ExceptionFunc : TypeAlias = Callable[[],ExceptionTuple|type(Exception)]


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


