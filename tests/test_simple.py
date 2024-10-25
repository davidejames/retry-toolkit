# SPDX-FileCopyrightText: © 2024 David E. James
# SPDX-License-Identifier: MIT
# SPDX-FileType: SOURCE

import time

import pytest

#-------------------------------------------------------------------------------
# Import the things we're testing:
#-------------------------------------------------------------------------------
from retry_toolkit.simple import (
    constant,     # basic backoff calculation functions
    linear,
    exponential,
    retry,        # the star of the show
    GiveUp,       # when retries still fail
    Defaults,     # module defaults
)


#-------------------------------------------------------------------------------
# Tests for Backoff Functions:
#-------------------------------------------------------------------------------

def test__constant():
    const_f = constant(2)
    assert const_f(0) == 2
    assert const_f(1) == 2
    assert const_f(2) == 2

    assert const_f(0.123) == 2


#┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
def test__linear():
    lin = linear(2)
    assert lin(0) == 0
    assert lin(1) == 2
    assert lin(2) == 4
    assert lin(3) == 6

    assert lin(0.123) == 0.246


#┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
def test__exponential():
    exp = exponential(2)

    assert exp(0) == 2
    assert exp(1) == 4
    assert exp(2) == 8
    assert exp(3) == 16


#-------------------------------------------------------------------------------
# Tests for Retry:
#-------------------------------------------------------------------------------

def test__default__no_issue():
    @retry()
    def foo():
        return 1

    assert foo() == 1


#┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
def test__default__tries():
    count = 0

    @retry()
    def foo():
        nonlocal count
        count += 1
        raise ValueError()

    with pytest.raises(GiveUp):
        foo()

    assert count == 3


#┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
# Testing Module Defaults
#┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
def test__default__altered_module_defaults_tries():
    count = 0

    @retry()
    def foo():
        nonlocal count
        count += 1
        raise ValueError()

    save_tries = Defaults.TRIES
    Defaults.TRIES = 5

    try:
        with pytest.raises(GiveUp):
            foo()
    except:
        pass
    finally:
        Defaults.TRIES = save_tries

    assert count == 5


#┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
def test__default__altered_module_defaults_sleep_func():
    count = 0

    @retry()
    def foo():
        nonlocal count
        count += 1
        raise ValueError()

    sleep_calls = 0

    def fake_sleep(t):
        nonlocal sleep_calls
        sleep_calls += 1

    save_sleep_f        = Defaults.SLEEP_FUNC
    Defaults.SLEEP_FUNC = fake_sleep

    try:
        with pytest.raises(GiveUp):
            foo()
    except:
        pass
    finally:
        Defaults.SLEEP_FUNC = save_sleep_f

    assert count       == 3   # # of total tries
    assert sleep_calls == 2   # # of re-tries


#┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
def test__default__altered_module_defaults_backoff():
    count = 0

    @retry()
    def foo():
        nonlocal count
        count += 1
        raise ValueError()

    sleep_t       = 0.0
    total_sleep_t = 0.0

    def fake_sleep(t):
        nonlocal sleep_t
        nonlocal total_sleep_t
        sleep_t = t
        total_sleep_t += t

    # setup fake sleep function again so test won't waste time
    save_sleep_f        = Defaults.SLEEP_FUNC
    Defaults.SLEEP_FUNC = fake_sleep

    # alter backoff
    save_backoff     = Defaults.BACKOFF
    Defaults.BACKOFF = 1

    try:
        with pytest.raises(GiveUp):
            foo()
    except:
        pass
    finally:
        Defaults.SLEEP_FUNC = save_sleep_f
        Defaults.BACKOFF    = save_backoff

    assert count         == 3      # number of total tries
    assert sleep_t       == 1.0    # last sleep reqested
    assert total_sleep_t == 2.0    # total sleep request (all re-tries)


#┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
def test__default__altered_module_defaults_exceptions():
    count = 0

    @retry()
    def foo():
        nonlocal count
        count += 1
        raise ValueError()

    def fake_sleep(t):
        pass

    # setup fake sleep function again so test won't waste time
    save_sleep_f        = Defaults.SLEEP_FUNC
    Defaults.SLEEP_FUNC = fake_sleep

    # limit exceptions for retrying:
    save_exc     = Defaults.EXC
    Defaults.EXC = (RuntimeError, BufferError)

    try:
        with pytest.raises(ValueError):
            foo()
    except:
        pass
    finally:
        Defaults.SLEEP_FUNC = save_sleep_f
        Defaults.EXC        = save_exc

    # the fact that a ValueError was raised outside of retry rather than
    # GiveUp is the point of this test


#┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
# Testing Retry Arguments
#┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
def test__arguments__tries():
    count = 0

    @retry(5)
    def foo():
        nonlocal count
        count += 1
        raise ValueError()

    with pytest.raises(GiveUp):
        foo()

    assert count == 5


#┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
def test__arguments__backoff():
    count = 0

    @retry(backoff=1.5)
    def foo():
        nonlocal count
        count += 1
        raise ValueError()

    sleep_t       = 0.0
    total_sleep_t = 0.0

    def fake_sleep(t):
        nonlocal sleep_t
        nonlocal total_sleep_t
        sleep_t = t
        total_sleep_t += t

    # setup fake sleep function again so test won't waste time
    save_sleep_f        = Defaults.SLEEP_FUNC
    Defaults.SLEEP_FUNC = fake_sleep

    try:
        with pytest.raises(GiveUp):
            foo()
    except:
        pass
    finally:
        Defaults.SLEEP_FUNC = save_sleep_f

    assert count         == 3      # number of total tries
    assert sleep_t       == 1.5    # last sleep reqested
    assert total_sleep_t == 3.0    # total sleep request (all re-tries)


#┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
def test__arguments__exceptions():
    count = 0

    my_exceptions = (RuntimeError, BufferError)
    @retry(exceptions=my_exceptions)
    def foo():
        nonlocal count
        count += 1
        raise ValueError()

    def fake_sleep(t):
        pass

    # setup fake sleep function again so test won't waste time
    save_sleep_f        = Defaults.SLEEP_FUNC
    Defaults.SLEEP_FUNC = fake_sleep

    try:
        with pytest.raises(ValueError):
            foo()
    except:
        pass
    finally:
        Defaults.SLEEP_FUNC = save_sleep_f

    # the fact that a ValueError was raised outside of retry rather than
    # GiveUp is the point of this test

