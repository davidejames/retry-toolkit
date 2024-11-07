from enum import Enum


class Events(Enum):
    SETUP   = 10
    START   = 20
    SKIP    = 30
    TRY     = 40
    FAIL    = 50
    ABORT   = 60
    GIVEUP  = 70
    SUCCESS = 80

    FAIL_ON_RESULT    = 51
    FAIL_ON_EXCEPTION = 52

    WARN_NEGATIVE_TRIES = 100
    WARN_NEGATIVE_SLEEP = 101



