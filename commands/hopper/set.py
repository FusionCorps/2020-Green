from typing import Union

from ctre import ControlMode
from wpilib.command import InstantCommand

from fusion.unique import unique
from subsystems import Hopper


@unique
class HopperSet(InstantCommand):
    def __init__(self, control_mode: ControlMode, value: Union[float, int]):
        super().__init__("HopperSet")

        self.requires(Hopper())

        self.control_mode = control_mode
        self.value = value

    def initialize(self):
        Hopper().set(self.control_mode, self.value)
