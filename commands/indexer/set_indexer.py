from wpilib.command import InstantCommand
from subsystems import indexer


class SetVelocity(InstantCommand):
    def __init__(self, velocity):
        super().__init__(__name__)
        self.velocity = velocity
        self.requires(indexer)

    def initialize(self):
        if not indexer.check_top():
            indexer.set_belt_velocity(velocity)


class SetPercentage(InstantCommand):
    def __init__(self, percentage):
        super().__init__("SetPercentage")
        self.requires(indexer)
        self.percentage = percentage

    def initialize(self):
        if not indexer.check_top():
            indexer.set_belt_percentage(self.percentage)


class SetPosition(InstantCommand):
    def __init__(self, ticks):
        super().__init__("SetPosition")
        self.ticks = ticks
        self.requires(indexer)

    def initialize(self):
        if not indexer.check_top():
            indexer.set_belt_ticks()

