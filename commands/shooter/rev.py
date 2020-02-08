from wpilib.command import InstantCommand
from subsystems.shooter import Shooter

class Rev(self, velocity):
    def __init__(self, velocity):
        super().__init__(__name__)
        self.velocity = velocity

    def initalize(self):
        Shooter.set_motors_velocity(velocity)
        