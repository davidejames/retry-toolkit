#┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅#
# SPDX-FileCopyrightText: © 2024 David E. James
# SPDX-License-Identifier: MIT
# SPDX-FileType: SOURCE
#┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈#

import inspect


#-------------------------------------------------------------------------------
# Private Utilities
#-------------------------------------------------------------------------------

def _ensure_callable(var, default):
    if callable(var):
        return var

    if var is not None:
        return lambda *args, **kwargs: var

    if callable(default) and not inspect.isclass(default):
        return default

    return lambda *args, **kwargs: default



def _get_async_callable(var, default):
    if callable(var):
        return var

    if var is not None:
        async def _var_f(*args, **kwargs):
            return var
        return _var_f

    if callable(default) and not inspect.isclass(default):
        return default

    async def _default_f(*args, **kwargs):
        return default

    return _default_f


def _ensure_async_callable(var, default):
    _callable = _get_async_callable(var, default)

    if not inspect.iscoroutinefunction(_callable):
        raise ValueError(f'coroutine is required for {var}/{default}')

    return _callable
