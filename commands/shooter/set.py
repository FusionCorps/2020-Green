from typing import Union

from ctre import ControlMode
from wpilib.command import InstantCommand

from fusion.unique import unique
from subsystems.shooter import Shooter


@unique
class ShooterSet(InstantCommand):
    def __init__(self, control_mode: ControlMode, value: Union[float, int]):
        super().__init__("ShooterSet")

        self.requires(Shooter())

        self.control_mode = control_mode
        self.value = value

    def initialize(self):
        Shooter().set(self.control_mode, self.value)

