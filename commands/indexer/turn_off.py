from wpilib.command import InstantCommand
from subsystems.indexer import Indexer
from fusion.unique import Unique


@Unique
class TurnOff(InstantCommand):
    def __init__(self):
        super().__init__("TurnOff")
        self.requires(Indexer())

    def initialize(self):
        Indexer().turn_off()

