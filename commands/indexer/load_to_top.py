from wpilib.command import Command
from subsystems.indexer import Indexer, IRService
from fusion.sensors import SensorService, Report, ReportError, Manager

class LoadToTop(Command):
    def initialize(self):
        Indexer.setBelt(1000)

    def isFinished(self):
        report = Manager().get(IRService, BreakReport)
        if report[2]:
            return True
    
    def end(self):
        Indexer.setBelt()
    

