from wpilib.command import InstantCommand
from subsystems import shooter

class TurnTurret(InstantCommand):
    def __init__(self, pos):
        super().__init__('TurnTurret')
        self.requires(shooter)
        self.pos = pos

    def initialize(self):
        shooter.set_turret(self.pos)