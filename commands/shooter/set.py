from ctre import ControlMode
from wpilib.command import InstantCommand

from fusion.unique import unique
from subsystems.shooter import Shooter


@unique
class SetVelocity(InstantCommand):
    def __init__(self, velocity: int):
        super().__init__("SetVelocity")
        self.requires(Shooter())

        self.velocity = velocity

    def initialize(self):
        Shooter().set(ControlMode.Velocity, self.velocity)


@unique
class SetPercentage(InstantCommand):
    def __init__(self, percentage: float):
        super().__init__("SetPercentage")
        self.requires(Shooter())

        self.percentage = percentage

    def initialize(self):
        Shooter().set(ControlMode.Velocity, self.percentage)
