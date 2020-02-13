from wpilib.command import Command
from subsystems.climb import Climb

class Climb(Command):
    def __init__(self):
        super().__init__("Climb")
        self.requires(Climb())

    def initialize(self):
        Climb().set_power_motor(0)

    def isFinished(self):
        if Climb().get_power_motor() == 0:
            return True

    def end(self):
        Climb().state = Climb.ClimbState.LOWERED
        

