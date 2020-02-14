from wpilib.command import Subsystem

from fusion.unique import unique


@unique
class Lift(Subsystem):
    def __init__(self):
        super().__init__("Lift")
