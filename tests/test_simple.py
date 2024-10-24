# SPDX-FileCopyrightText: 2024-present David E. James <david.eugene.james@protonmail.com>
#
# SPDX-License-Identifier: MIT

import time

import pytest

#-------------------------------------------------------------------------------
# Import the things we're testing:
#-------------------------------------------------------------------------------
from retry_toolkit.simple import (
    # --- basic backoff calculations
    linear,
    exponential,
    # --- the star of the show
    retry,
    # --- exception
    GiveUp,
    # --- defaults
    Defaults,
)


#-------------------------------------------------------------------------------
# Tests for Backoff Functions:
#-------------------------------------------------------------------------------

def test__exponential():
    exp = exponential(2)

    assert exp(0) == 2
    assert exp(1) == 4
    assert exp(2) == 8
    assert exp(3) == 16


def test__linear():
    lin = linear(2)
    assert lin(0) == 0
    assert lin(1) == 2
    assert lin(2) == 4
    assert lin(3) == 6

    assert lin(0.123) == 0.246


#-------------------------------------------------------------------------------
# Tests for Retry:
#-------------------------------------------------------------------------------

def test__default__no_issue():
    @retry()
    def foo():
        return 1

    assert foo() == 1


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


def test__default__altered_module_defaults():
    count = 0

    @retry()
    def foo():
        nonlocal count
        count += 1
        raise ValueError()

    Defaults.TRIES = 5

    with pytest.raises(GiveUp):
        foo()

    assert count == 5
