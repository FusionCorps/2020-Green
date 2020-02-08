from wpilib.command import InstantCommand
from subsystems.shooter import Shooter

class Rev(self, velocity):
    def __init__(self, per):
        super().__init__(__name__)
        self.velocity = per

    def initalize(self):
        Shooter.set_motors_percentage(per)
