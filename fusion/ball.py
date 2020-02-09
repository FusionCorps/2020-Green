from typing import *

from enum import Enum


class Ball:
    balls: List = None

    class Position(Enum):
        INTAKE = 0
        HOPPER = 1
        INDEXER = 2
        SHOOTER = 3

    def __init__(self):
        if Ball.balls is None:
            balls = []
