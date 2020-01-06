from wpilib.command import Command

from inputs import controller
from subsystems import i_chassis


class JoystickDrive(Command):
    def __init__(self):
        super().__init__(name="JoystickDrive", timeout=0.0, subsystem=i_chassis)

    def initialize(self):
        return super().initialize()

    def execute(self):
        i_chassis.joystick_drive(controller.get_x(), controller.get_y())

    def isFinished(self):
        return super().isFinished()

    def end(self):
        i_chassis.drive.stopMotor()

    def interrupted(self):
        self.end()
