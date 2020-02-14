from wpilib.command import Command

from fusion.unique import unique
from subsystems import Indexer, Shooter


@unique
class Shoot(Command):
    def __init__(self):
        super().__init__(__name__)
        self.requires(Shooter())

    def initialize(self):
        if Shooter().state == Shooter().State.WAITING:
            Indexer().set_vert_belt(True, 2000)
            Shooter().state = Shooter().State.SHOOTING

    def execute(self):
        # Check if belt is still moving
        pass

    def isFinished(self):
        return False
        # report = Manager().get(IRService, BreakReport)
        # if report[2]:
        #     return True

    def end(self):
        Shooter().state = Shooter().State.WAITING
