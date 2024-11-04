#┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅#
# SPDX-FileCopyrightText: © 2024 David E. James
# SPDX-License-Identifier: MIT
# SPDX-FileType: SOURCE
#┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈#

import asyncio
import time


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
    RETRY_CLASS = None
    '''class to use for all class-based retry logic.'''

    ASYNC_RETRY_CLASS = None
    '''class to use for all async-class-based retry logic.'''

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

    ASYNC_SLEEP_FUNC = asyncio.sleep
    '''callable: used as async sleep waiter'''



class AsyncDefaults:
    '''Defaults for retry behavior async variant

    These values are used if not specified during retry decorator generation
    or if not overriden here (sleep function). For these defaults, it is
    also acceptable to set them to a callable returning the required type
    using the same convention as if it were used as an argument to the
    retry decorator generator.
    '''
    RETRY_CLASS = None
    '''class to use for all class-based retry logic.'''

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

    SLEEP_FUNC = asyncio.sleep
    '''callable: used as async sleep waiter'''

