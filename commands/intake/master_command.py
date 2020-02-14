from wpilib.command import Command
from subsystems import intake

class MasterCommand(Command):

    def __init__(self):
        super().__init__('MasterCommand')
        self.requires(Intake())

    def execute(self):
    #     if Rithuik camera thingy:
    #         do the wrrrrrrrr

        pass
