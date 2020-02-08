from wpilib.command import Command
from subsystems.shooter import Shooter
from subsystems.indexer import Indexer
from fusion.sensors import Manager

class Shoot(Command):

    BALL_DIAMETER = 0.2 # m 
    WHEEL_RADIUS = 0.009525

    REQUIRED_TICKS = BALL_DIAMETER*2048/2/pi/WHEEL_RADIUS

    def __init__(self):
        super().__init__(__name__)
        self.requires(Shooter())
        self.requires(Indexer())

    def initialize(self):
        if Shooter().state == Shooter().State.WAITING:
            Indexer().set_belt_ticks(Shoot.REQUIRED_TICKS)
            Shooter().state = Shooter().State.SHOOTING

    def execute(self):
        # Check if belt is still moving
        pass

    def isFinished(self):
        report = Manager().get(IRService, BreakReport)
        if report[2]:
            return True
    
    def end(self):
        Shooter().state = Shooter().State.SPOOLING

    


