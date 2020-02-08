from wpilib.command import Subsystem

from ctre import WPI_VictorSPX, ControlMode


class Hopper(Subsystem):
    ID_HOPPER_CONTROLLER = 0

    def __init__(self):
        super().__init__("Hopper")

        self._hopper_controller = WPI_VictorSPX(Hopper.ID_HOPPER_CONTROLLER)

    def set(self, control_mode: ControlMode, value):
        self._hopper_controller.set(control_mode, value)
