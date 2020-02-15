from wpilib.command import InstantCommand

from fusion.unique import unique
from subsystems import Lift


@unique
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
