from wpilib.command import InstantCommand
from subsystems.indexer import Indexer


class SetVelocity(InstantCommand):
    def __init__(self, velocity):
        super().__init__(__name__)
        self.velocity = velocity
        self.requires(Indexer())

    def initialize(self):
        if not Indexer().check_top():
            Indexer().set_belt_velocity(velocity)


class SetPercentage(InstantCommand):
    def __init__(self, percentage):
        super().__init__("SetPercentage")
        self.requires(Indexer())
        self.percentage = percentage

    def initialize(self):
        if not Indexer().check_top():
            Indexer().set_belt_percentage(self.percentage)


class SetPosition(InstantCommand):
    def __init__(self, ticks):
        super().__init__("SetPosition")
        self.ticks = ticks
        self.requires(Indexer())

    def initialize(self):
        if not Indexer().check_top():
            Indexer().set_belt_ticks()

