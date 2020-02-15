import logging
from wpilib.command import Command

from inputs import XBoxController
from subsystems import Chassis

from fusion.unique import unique


@unique
class ChassisJoystickDrive(Command):
    def __init__(self):
        super().__init__("JoystickDrive")
        self.requires(Chassis())
        self.logger = logging.getLogger("JoystickDrive")

    def execute(self):
        Chassis()._drive.curvatureDrive(
            XBoxController().l_stick_vert * 0.5,
            XBoxController().r_stick_horiz * 0.5,
            True,
        )

    def isFinished(self):
        return False

    def interrupted(self):
        self.end()
