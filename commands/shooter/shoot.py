from wpilib.command import Command

from fusion.unique import Unique
from subsystems import Indexer, Shooter


@Unique
class Shoot(Command):
    def __init__(self):
        super().__init__(__name__)
        self.requires(Shooter())

    def initialize(self):
        if Shooter().state == Shooter().State.WAITING:
            Indexer().set_vert_belt(True, 2000)
            Shooter().state = Shooter().ShooterState.SHOOTING

    def execute(self):
        # Check if belt is still moving
        pass

    def isFinished(self):
        return False
        # report = Manager().get(IRService, BreakReport)
        # if report[2]:
        #     return True

    def end(self):
        Shooter().state = Shooter().ShooterState.WAITING
