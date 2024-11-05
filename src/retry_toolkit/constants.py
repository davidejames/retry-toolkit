from enum import Enum

class Warnings(Enum):
    NEGATIVE_TRIES = 10
    NEGATIVE_SLEEP = 20


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

