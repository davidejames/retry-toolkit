#┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅#
# SPDX-FileCopyrightText: © 2024 David E. James
# SPDX-License-Identifier: MIT
# SPDX-FileType: SOURCE
#┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈#

import inspect
from collections import defaultdict

from .defaults import LoggingDefaults


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


def _apply(item, func):
    if isinstance(item, list):
        for _item in item:
            func(_item)
    else:
        func(item)


async def _async_call_f(func, *args, **kwargs):
    if inspect.iscoroutinefunction(func):
        return await func(*args, **kwargs)
    return func(*args, **kwargs)


def _get_logging_subscribers(logging_config=None, logger=None):
    _logging_config = logging_config or LoggingDefaults.LOG_CONFIG
    _default_logger = LoggingDefaults.LOGGER
    _default_level  = LoggingDefaults.LOG_LEVEL
    _default_msg_t  = LoggingDefaults.LOG_MSG_T

    subscriptions = dict()

    for key, cfg in _logging_config.items():
        logger_f = _ensure_callable(cfg.get('logger'), _default_logger)
        level_f  = _ensure_callable(cfg.get('level '), _default_level )
        msg_t_f  = _ensure_callable(cfg.get('msg_t' ), _default_msg_t )

        def _log(event, obj, context, *args, **kwargs):
            logger = logger_f(event=event, obj=obj, context=context)
            level  = level_f( event=event, obj=obj, context=context)
            msg_t  = msg_t_f( event=event, obj=obj, context=context)

            msg = msg_t.format(event=event.name, **context)
            logger.log(level, msg, extra=kwargs)

        subscriptions[key] = _log

    return subscriptions



class PubSubManager:
    def __init__(self, enum_obj, subscriptions):
        self.event_list = list(enum_obj)
        self.subs = {e:[] for e in self.event_list}

        self.subscribe_all(subscriptions)


    def subscribe(self, event, subscriber):
        BAD_TYPE_MSG = '{s} is invalid subscription for {e}'
        INVALID_MSG  = '{s} is not a valid event'
        SUCCESS_MSG  = '{s} subscribed to {e}'

        successes  = []
        warnings = []

        def _sub(event, sub):
            if not callable(sub):
                warnings.append(BAD_TYPE_MSG.format(s=sub, e=event))
            else:
                subs[event].append(sub)
                successes.append(SUCCESS_MSG.format(v=sub, e=event))

        _apply(subscriber, _sub)

        return successes, warnings


    def unsubscribe(self, event, subscriber):
        successes = []
        warnings  = []

        def _unsubscribe(event, sub):
            _subs = self.subs[event]
            if sub not in _subs:
                warnings.append('not a subscriber')
            else:
                _subs.remove(sub)
                successes.append(f'removed {sub}')

        _apply(subscriber, _unsubscribe)

        return successes, warnings


    def subscribe_all(self, subscriptions):
        if subscriptions is None:
            return

        if not isinstance(subscriptions, dict):
            raise ValueError('subscriptions must be a dictionary')

        INVALID_MSG  = '{v} is not a valid event'

        successes = []
        warnings  = []

        #┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈
        for event in self.subs.keys():
            _sub = subscriptions.get(event)
            if _sub is None:
                continue

            _s, _w = self.subscribe(event, _sub)

            successes.extend(_s)
            warnings.extend(_w)

        #┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈
        for key in subscriptions:
            if not isinstance(key, enum_obj):
                warnings.append(INVALID_MSG.format(e=key))

        return successes, warnings


    async def async_publish(self, event, subscriptions, *args, **kwargs):
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


    def publish(self, event, context, *args, **kwargs):
        _subs = self.subs.get(event)
        if _subs is None:
            return

        errors = []
        for _sub in _subs:
            try:
                _sub(event, context, *args, **kwargs)
            except Exception as e:
                errors.append(e)

        return errors


