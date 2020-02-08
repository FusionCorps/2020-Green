from wpilib.command import InstantCommand
from subsystems.intake import Intake

class TurnOff(InstantCommand):

    def initiate(self):
        Intake().turn_off()