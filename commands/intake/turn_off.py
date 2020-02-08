from wpilib.command import InstantCommand
from subsystems.intake import Intake

class TurnOff(InstantCommand):

    def __init__(self):
        super().__init__('TurnOff')
        self.requires(Intake())

    def initiate(self):
        Intake().turn_off()