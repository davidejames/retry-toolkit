#┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅#
# SPDX-FileCopyrightText: © 2024 David E. James
# SPDX-License-Identifier: MIT
# SPDX-FileType: SOURCE
#┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈#

import inspect
from collections import defaultdict


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


async def _async_call_f(func, *args, **kwargs):
    if inspect.iscoroutinefunction(func):
        return await func(*args, **kwargs)
    return func(*args, **kwargs)


def _process_subscriptions(enum_obj, subscriptions):
    subs = defaultdict(list)

    if subscriptions is None:
        return subs

    if not isinstance(subscriptions, dict):
        raise ValueError('subscriptions must be a dictionary')

    BAD_TYPE_MSG = '{v} is invalid subscription for {e}'
    INVALID_MSG  = '{v} is not a valid event'
    SUCCESS_MSG  = '{v} subscribed to {e}'

    success  = []
    warnings = []

    #┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈
    def _success(v, e):
        success.append(SUCCESS_MSG.format(v=v, e=e))

    #┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈
    def _warn(msg, v, e=None):
        warnings.append(msg.format(v=v, e=e))

    #┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈
    def _subscribe(event, item):
        if not callable(_s):
            _warn(BAD_TYPE_MSG, _s, event)
        else:
            subs[event].append(_s)
            _success(_s, event)

    #┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈
    for event in list(Events):
        _sub = subscriptions.get(event)
        if isinstance(_sub, list):
            for _s in _sub:
                _subscribe(event, _s)
        else:
            _subscribe(event, _s)

    #┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈
    for key in subscriptions:
        if not isinstance(key, enum_obj):
            _warn(INVALID_MSG, key)

    return success, warnings, subs


async def _async_publish(event, subscriptions, *args, **kwargs):
    _subs = subscriptions.get(event)
    if _subs is None:
        return

    errors = []
    for _sub in _subs:
        try:
            await _acall_f(_sub, event, context, *args, **kwargs)
        except Exception as e:
            errors.append(e)

    return errors



def _publish(event, subscriptions, context, *args, **kwargs):
    _subs = subscriptions.get(event)
    if _subs is None:
        return

    errors = []
    for _sub in _subs:
        try:
            _sub(event, context, *args, **kwargs)
        except Exception as e:
            errors.append(e)

    return errors


def _get_logging_subscriptions(logging_config=None):
    _logging_config = logging_config or LoggingDefaults.LOG_CONFIG
    subscriptions = dict()
    for key, cfg in logging_config.items():
        logger = cfg.get('logger' , LoggingDefaults.LOGGER    )
        level  = cfg.get('level'  , LoggingDefaults.LOG_LEVEL )
        msg_t  = cfg.get('msg_t'  , LoggingDefaults.LOG_MSG_T )

        def _log(event, obj, context, *args, **kwargs):
            msg = msg_t.format(event=event.name, **context)
            logger.log(level, msg, extra=kwargs)

        subscriptions[key] = _log

    return subscriptions


