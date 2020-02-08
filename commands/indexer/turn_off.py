from wpilib.command import InstantCommand
from subsystems.indexer import Indexer

class TurnOff(InstantCommand):
def __init__(self):
    super().__init__(__name__)
    self.requires(Indexer)


    def initalize(self):
        Indexer().turn_off()