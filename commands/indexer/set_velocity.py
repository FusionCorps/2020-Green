from wpilib.command import InstantCommand
from subsystems.indexer import Indexer

class SetVelocity(InstantCommand):
    def __init__(self, velocity):
        super().__init__(__name__)
        self.velocity = velocity
        self.requires(Indexer)

    def initialize(self):
        Indexer().set_belt_velocity(velocity)
