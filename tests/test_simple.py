
from retry_toolkit.simple import (
    linear,
    exponential,
    retry,
)

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



def test__default__no_issue():
    @retry()
    def foo():
        return 1

    assert foo() == 1



