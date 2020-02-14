from wpilib.command import InstantCommand
from subsystems import indexer

class TurnOff(InstantCommand):
    def __init__(self):
        super().__init__(__name__)
        self.requires(indexer)


        def initalize(self):
            indexer.turn_off()