from wpilib.command import InstantCommand
from subsystems.hopper import Hopper

class TurnOff(InstantCommand):
    def __init__(self):
        super().__init__('TurnOff')
        self.requires(Hopper())

    def initialize(self):
        Hopper().turn_off()

