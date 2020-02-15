from wpilib.command import Command

from inputs import xbox_controller
from subsystems import Chassis

from fusion.unique import unique


@unique
class JoystickDrive(Command):
    def __init__(self):
        super().__init__(name="JoystickDrive", timeout=0.0, subsystem=Chassis())

    def execute(self):
        Chassis().joystick_drive(xbox_controller.x.get(), xbox_controller.y.get())

    def end(self):
        Chassis().drive.stopMotor()

    def interrupted(self):
        self.end()
