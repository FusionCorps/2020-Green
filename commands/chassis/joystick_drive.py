from wpilib.command import Command

from inputs import controller
from subsystems.chassis import Chassis


class JoystickDrive(Command):
    def __init__(self):
        super().__init__(name="JoystickDrive", timeout=0.0, subsystem=Chassis())

    def initialize(self):
        return super().initialize()

    def execute(self):
        Chassis().joystick_drive(controller.get_x(), controller.get_y())

    def isFinished(self):
        return super().isFinished()

    def end(self):
        Chassis().drive.stopMotor()

    def interrupted(self):
        self.end()
