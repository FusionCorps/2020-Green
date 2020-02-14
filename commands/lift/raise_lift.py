from wpilib.command import InstantCommand

from fusion.unique import Unique
from subsystems import Lift


@Unique
class RaiseLift(InstantCommand):
    def __init__(self, distance):
        super().__init__("RaiseLift")

        self.distance = distance
        self.requires(Lift())

    def initiate(self):
        Lift().turn_ticks(self.distance)
        Lift().state = Lift().ClimbState.RISING

    def end(self):
        Lift().state = Lift().ClimbState.RAISED
