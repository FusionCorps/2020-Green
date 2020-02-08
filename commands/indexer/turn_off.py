from wpilib.command import InstantCommand
from subsystems.indexer import Indexer

class TurnOff(InstantCommand):
    def initalize(self):
        Indexer.turn_off()