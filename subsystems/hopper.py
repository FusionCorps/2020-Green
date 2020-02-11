from wpilib.command import Subsystem

from ctre import WPI_VictorSPX, ControlMode


class Hopper(Subsystem):
    _instance = None

    ID_HOPPER_CONTROLLER = 0

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Hopper, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        super().__init__("Hopper")

        self._hopper_controller = WPI_VictorSPX(Hopper.ID_HOPPER_CONTROLLER)

    def set(self, control_mode: ControlMode, value):
        self._hopper_controller.set(control_mode, value)

