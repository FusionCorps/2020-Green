from ctre import ControlMode
from wpilib.command import Command, InstantCommand

import subsystems

import inputs


class SetJoystick(Command):
    def __init__(self):
        super().__init__("SetJoystick")
        self.requires(subsystems.Intake())

    def execute(self):
        subsystems.Intake().set(
            ControlMode.PercentOutput, inputs.XBoxController().axis_l_trigger
        )

    def interrupted(self):
        self.end()

    def end(self):
        subsystems.Intake().set(ControlMode.PercentOutput, 0.0)


class SetPercentage(InstantCommand):
    def __init__(self, percentage: float):
        super().__init__("SetPercentage")
        self.requires(subsystems.Intake())

        self.percentage = percentage

    def initialize(self):
        subsystems.Intake().set(ControlMode.PercentOutput, self.percentage)

