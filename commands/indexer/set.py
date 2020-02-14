from wpilib.command import InstantCommand
from subsystems import Indexer

from fusion.unique import Unique


@Unique
class SetVelocity(InstantCommand):
    def __init__(self, velocity):
        super().__init__(__name__)

        self.velocity = velocity
        self.requires(Indexer())

    def initialize(self):
        Indexer().set_belt_velocity(self.velocity)


@Unique
class SetPercentage(InstantCommand):
    def __init__(self, percentage):
        super().__init__("SetPercentage")

        self.requires(Indexer())
        self.percentage = percentage

    def initialize(self):
        Indexer().set_belt_percentage(self.percentage)


@Unique
class SetPosition(InstantCommand):
    def __init__(self, ticks):
        super().__init__("SetPosition")

        self.ticks = ticks
        self.requires(Indexer())

    def initialize(self):
        Indexer().set_belt_ticks()
