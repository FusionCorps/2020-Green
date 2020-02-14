from wpilib.command import Command
from subsystems.climb import Climb
from ctre import ControlMode

class Climb(Command):
    def __init__(self):
        super().__init__("Climb")
        self.requires(climb)

    def initialize(self):
        climb.set_climb_motor(ControlMode.MotionMagic, 0)

    def isFinished(self):
        if climb.get_climb_motor() == 0:
            return True

    def end(self):
        climb.state = Climb.ClimbState.LOWERED
        

