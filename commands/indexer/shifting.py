from wpilib.command import Command
from subsystems.indexer import Indexer, IRService
from fusion.sensors import SensorService, Report, ReportError, Manager
from math import pi
from subsystems import indexer

class ShiftOneForward(Command):

    BALL_DIAMETER = 0.2 # m 
    WHEEL_RADIUS = 0.009525

    REQUIRED_TICKS = BALL_DIAMETER*2048/2/pi/0.009525

    def __init__(self, pass_check:bool = False):
        super().__init__(__name__)
        self.requires(indexer)
        self.pass_check = pass_check

    def initialize(self):
        if not indexer.check_top() or self.pass_check:
            indexer.set_belt_ticks(REQUIRED_TICKS)
            for ball in indexer.ball_list:
                ball += 1
                if ball == 6:
                    indexer.ball_list.pop()
                if indexer.check_entry():
                    indexer.ball_list.insert(1)
            
                

    def isFinished(self):
        if indexer.belt_controller.get() == 0:
            return True
    
    def end(self):
        pass
    
class ShiftOneBack(Command):

    def __init__(self):
        super().__init__('ShiftOneBack')
        self.requires(indexer)

    def initialize(self):
        indexer.set_belt_ticks(-1*(ShiftOneForward.REQUIRED_TICKS))
        for ball in indexer.ball_list:
            ball -= 1
            if ball == 0:
                indexer.ball_list.pop(0)

    def isFinished(self):
        if indexer.belt_controller.get() == 0:
            return True

    
