from wpilib.command import Command
from subsystems.intake import Intake

class TurnOff(Command):

    def initiate(self):
        Intake.turn_off()