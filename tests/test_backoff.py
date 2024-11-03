# SPDX-FileCopyrightText: © 2024 David E. James
# SPDX-License-Identifier: MIT
# SPDX-FileType: SOURCE

import time

import pytest

#-------------------------------------------------------------------------------
# Import the things we're testing:
#-------------------------------------------------------------------------------
from retry_toolkit.backoff import (
    constant,     # basic backoff calculation functions
    linear,
    exponential,
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



