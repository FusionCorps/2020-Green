from typing import List

from ctre import WPI_VictorSPX, ControlMode
from wpilib.command import Subsystem
from wpilib.drive import DifferentialDrive


class Intake(Subsystem):
    ID_INTAKE_CONTROLLER = 0

    def __init__(self):
        super().__init__("Intake")

        self._intake_controller = WPI_VictorSPX(Intake.ID_INTAKE_CONTROLLER)

    def set(self, control_mode: ControlMode, value):
        self._intake_controller.set(control_mode, value)

    def initDefaultCommand(self):
        from commands import SetJoystick

        self.setDefaultCommand(SetJoystick)
