from wpilib.command import Command
from subsystems import indexer, IRService, BreakReport
from fusion.sensors import Manager
from commands.indexer import ShiftOverOne

class MasterCommand(Command):

    def __init__(self):
        super().__init__('MasterCommand')
        self.requires(Indexer())

    def initialize(self):
        pass

    def execute(self):
        report = Manager().get(IRService, BreakReport)
        if report[0]:
            ShiftOverOne().start()
    
    def end(self):
        pass

    def isFinished(self):
        # Button command or something, I don't know
        pass

    

        

master_command = MasterCommand()
