from wpilib.command import Command
from subsystems.indexer import Indexer, IRService
from fusion.sensors import SensorService, Report, ReportError, Manager


class ShiftOneForward(Command):

    BALL_DIAMETER = 0.2 # m 
    WHEEL_RADIUS = 0.009525

    REQUIRED_TICKS = BALL_DIAMETER*2048/2/pi/0.009525

    def __init__(self):
        super().__init__(__name__)
        self.requires(Indexer())

    def initialize(self):
        if not Indexer().check_top():
            Indexer().set_belt_ticks(REQUIRED_TICKS)

    def isFinished(self):
        if Indexer().belt_controller.get() == 0:
            return True
    
    def end(self):
        pass
    
class ShiftOneBack(Command):

    def __init__(self):
        super().__init__('ShiftOneBack')
        self.requires(Indexer())

    def initialize(self):
        Indexer().set_belt_ticks(-1*(REQUIRED_TICKS))

    def isFinished(self):
        if Indexer().belt_controller.get() == 0:
            retrun True

    