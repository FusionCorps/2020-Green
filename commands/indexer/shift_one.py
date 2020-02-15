from math import pi

from ctre import ControlMode
from wpilib.command import Command

from functools import lru_cache
from subsystems import Indexer


class ShiftOverOneSlot(Command):
    BALL_DIAMETER = 0.2  # m
    WHEEL_RADIUS = 0.009525

    REQUIRED_TICKS = BALL_DIAMETER * 2048 / 2 / pi / 0.009525

    @lru_cache(maxsize=None)
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self):
        super().__init__("ShiftOverOneSlot")

        self.requires(Indexer())

    def initialize(self):
        Indexer().zero_encoder()
        Indexer().set(ControlMode.Position, ShiftOverOneSlot.REQUIRED_TICKS)

    def isFinished(self):
        if Indexer().get_position() == ShiftOverOneSlot.REQUIRED_TICKS:
            return True

    def end(self):
        pass
