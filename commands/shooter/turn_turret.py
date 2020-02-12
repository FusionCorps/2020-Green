from wpilib.command import InstantCommand
from subsystems.shooter import Shooter

class TurnTurret(InstantCommand):
    def __init__(self, pos):
        super().__init__('TurnTurret')
        self.requires(Shooter())
        self.pos = pos

    def initialize(self):
        Shooter().set_turret(self.pos)