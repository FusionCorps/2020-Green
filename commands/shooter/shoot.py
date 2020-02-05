from wpilib.command import Command
from subsystems.shooter import Shooter
from subsystems.indexer import Indexer
from fusion.sensors import Manager

class Shoot(Command):

    def initialize(self):
        if Shooter().state == Shooter().State.WAITING:
            Indexer.set_vert_belt(True, 2000):
            Shooter().state = Shooter().State.SHOOTING

    def execute(self):
        # Check if belt is still moving
        pass

    def isFinished(self):
        report = Manager().get(IRService, BreakReport)
        if report[2]:
            return True
    
    def end(self):
        Shooter().state = Shooter().State.WAITING

    


