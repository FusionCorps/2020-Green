from wpilib.command import InstantCommand
from subsystems.indexer import Indexer
from functools import lru_cache


class TurnOff(InstantCommand):
    @lru_cache(maxsize=None)
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self):
        super().__init__("TurnOff")
        self.requires(Indexer())

    def initialize(self):
        Indexer().turn_off()

