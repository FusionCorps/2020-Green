from wpilib.command import InstantCommand
from subsystems.intake import Intake

class SetIntake(InstantCommand):
    def __init__(self, velocity):
        super().__init__("SetIntake")
        self.requires(Intake())
        self.velocity = velocity

    def initiate(self):
        Intake().set_intake(self.velocity)
    

