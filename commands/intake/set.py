from fusion.unique import unique
from ctre import ControlMode
from wpilib.command import Command, InstantCommand

from subsystems import Intake
import inputs


@unique
class SetJoystick(Command):
    def __init__(self):
        super().__init__("SetJoystick")

        self.requires(Intake())

    def execute(self):
        Intake().set(ControlMode.PercentOutput, inputs.XBoxController().axis_l_trigger)

    def interrupted(self):
        self.end()

    def end(self):
        Intake().set(ControlMode.PercentOutput, 0.0)


@unique
class SetPercentage(InstantCommand):
    def __init__(self, percentage: float):
        super().__init__("SetPercentage")

        self.requires(Intake())

        self.percentage = percentage

    def initialize(self):
        Intake().set(ControlMode.PercentOutput, self.percentage)
