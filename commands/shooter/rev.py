from wpilib.command import InstantCommand
from subsystems import shooter

class Rev(self, velocity):
    def __init__(self, per):
        super().__init__(__name__)
        self.velocity = per
        self.requires(shooter)

    def initalize(self):
        shooter.set_motors_percentage(per)
