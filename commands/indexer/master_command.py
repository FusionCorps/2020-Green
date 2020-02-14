from wpilib.command import Command
from subsystems import Indexer, IRService, BreakReport, Shooter, Hopper
from fusion.sensors import Manager
from commands.indexer import ShiftOverOne
from _pynetworktables import NetworkTable

class MasterCommand(Command):

    def __init__(self):
        super().__init__('MasterCommand')
        self.requires(Indexer())

    def initialize(self):
        pass

    def execute(self):
        report = Manager().get(IRService, BreakReport)
        ready_to_shoot = False
        if NetworkTable.getTable("limelight").getNumber('tx') == 0 and Shooter().get_state() == Shooter.State.WAITING:
            ready_to_shoot = True
        ShiftOverOne(ready_to_shoot).start() # Winston, can you check to make sure I am doing this right?

        

        
    
    def end(self):
        pass

    def isFinished(self):
        # Button command or something, I don't know
        pass

    

        

master_command = MasterCommand()
