from wpilib.command import InstantCommand

from ctre import ControlMode

import subsystems


class SetPercentage(InstantCommand):
    def __init__(self, percentage: float):
        super().__init__("SetPercentage")
        self.requires(subsystems.Hopper())

        self.percentage = percentage

    def initialize(self):
        subsystems.Hopper().set(ControlMode.PercentOutput, self.percentage)
