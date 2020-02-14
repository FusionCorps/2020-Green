
from wpilib.command import InstantCommand
from subsystems import hopper

class TurnOff(InstantCommand):
    def __init__(self):
        super().__init__('TurnOff')
        self.requires(hopper)

    def initialize(self):
        hopper.turn_off()