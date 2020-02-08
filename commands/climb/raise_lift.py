from wpilib.command import InstantCommand
from subsystems.climb import Climb

class RaiseLift(Command):
    def __init__(self, distance):
        super.__init__('RaiseLift')
        self.distance = distance
        self.requires(Climb())

    def initiate(self):
        Climb().turn_ticks(distance)
        Climb().state = Climb().ClimbState.RISING

    def end(self):
        Climb().state = Climb().ClimbState.RAISED

    def execute(self):
        pass

    def isFinished(self):
        if Climb().climb_controller.get() == 0.0:
            return True

    
