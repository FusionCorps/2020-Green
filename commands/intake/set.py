from typing import Union

from ctre import ControlMode
from wpilib.command import Command, InstantCommand

import inputs
from fusion.unique import unique
from subsystems import Intake


@unique
class IntakeJoystickSet(Command):
    def __init__(self):
        super().__init__("IntakeJoystickSet")

        self.requires(Intake())

    def execute(self):
        Intake().set(
            ControlMode.PercentOutput,
            inputs.XBoxController().axis_l_trigger
            - inputs.XBoxController().axis_r_trigger,
        )

    def interrupted(self):
        self.end()

    def end(self):
        Intake().set(ControlMode.PercentOutput, 0.0)


@unique
class IntakeSet(InstantCommand):
    def __init__(self, control_mode: ControlMode, value: Union[float, int]):
        super().__init__("IntakeSet")

        self.requires(Intake())

        self.control_mode = control_mode
        self.value = value

    def initialize(self):
        Intake().set(self.control_mode, self.value)
