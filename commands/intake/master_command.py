from wpilib.command import Command
from subsystems import intake
from fusion import VirtualBall

class MasterCommand(Command):

    def __init__(self):
        super().__init__('MasterCommand')
        self.requires(Intake())

    def execute(self):
        # if Rithuik camera thingy:
        #     do the wrrrrrrrr
        #     Intake().ball_list.insert(VirtualBall())
        # if rithuik camera thingy II:
        #     Intake().ball_list[-1].state = VirtualBall.BallState.HOPPER
        #     Hopper().ball_list.insert(Intake().ball_list[-1])
        #     Intake().ball_list.pop()
    
        pass
