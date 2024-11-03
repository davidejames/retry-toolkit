#┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅#
# SPDX-FileCopyrightText: © 2024 David E. James
# SPDX-License-Identifier: MIT
# SPDX-FileType: SOURCE
#┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈#

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



