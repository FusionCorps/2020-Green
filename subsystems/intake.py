from ctre import ControlMode, WPI_VictorSPX
from wpilib.command import Subsystem

from fusion.unique import unique


@unique
class Intake(Subsystem):
    ID_INTAKE_CONTROLLER = 0

    def __init__(self):
        super().__init__("Intake")

        self._intake_controller = WPI_VictorSPX(Intake.ID_INTAKE_CONTROLLER)

    def set(self, control_mode: ControlMode, value):
        self._intake_controller.set(control_mode, value)

    def initDefaultCommand(self):
        from commands.intake import SetJoystick

        self.setDefaultCommand(SetJoystick())
