from wpilib.command import Command
from subsystems.indexer import Indexer, IRService
from fusion.sensors import SensorService, Report, ReportError, Manager
from math import pi


class ShiftOneForward(Command):

    BALL_DIAMETER = 0.2 # m 
    WHEEL_RADIUS = 0.009525

    REQUIRED_TICKS = BALL_DIAMETER*2048/2/pi/0.009525

    def __init__(self, pass_check:bool = False):
        super().__init__(__name__)
        self.requires(Indexer())
        self.pass_check = pass_check

    def initialize(self):
        if not Indexer().check_top() or self.pass_check:
            Indexer().set_belt_ticks(REQUIRED_TICKS)
            for ball in Indexer().ball_list:
                ball += 1
                if ball == 6:
                    Indexer().ball_list.pop()
                if Indexer().check_entry():
                    Indexer().ball_list.insert(1)
            
                

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
        Indexer().set_belt_ticks(-1*(ShiftOneForward.REQUIRED_TICKS))
        for ball in Indexer().ball_list:
            ball -= 1
            if ball == 0:
                Indexer().ball_list.pop(0)

    def isFinished(self):
        if Indexer().belt_controller.get() == 0:
            return True

    
