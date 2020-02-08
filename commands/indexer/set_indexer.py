from wpilib.command import InstantCommand
from subsystems.indexer import Indexer

class SetVelocity(InstantCommand):
    def __init__(self, velocity):
        super().__init__(__name__)
        self.velocity = velocity
        self.requires(Indexer())

    def initialize(self):
        Indexer().set_belt_velocity(velocity)

class SetPercentage(InstantCommand):
    def __init__(self, percentage):
        super().__init__('SetPercentage')
        self.requires(Indexer())
        self.percentage = percentage

    def initalize(self):
        Indexer().set_belt_percentage(self.percentage)

class SetTicks(InstantCommand):
    def __init__(self, ticks):
        super().__init__('SetTicks')
        self.ticks = ticks
        self.requires(Indexer())

    def initialize(self):
        Indexer().set_belt_ticks()

