from ctre import ControlMode
from wpilib.command import InstantCommand

from functools import lru_cache
from subsystems import Hopper

from fusion.unique import unique


@unique
class SetPercentage(InstantCommand):
    def __init__(self, percentage: float):
        super().__init__("SetPercentage")

        self.requires(Hopper())
        self.percentage = percentage

    def initialize(self):
        Hopper().set(ControlMode.PercentOutput, self.percentage)
