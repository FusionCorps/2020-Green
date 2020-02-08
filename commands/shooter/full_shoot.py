from subsystems.shooter import Shooter
from wpilib.command import Command


class FullShoot(Command):

    def __init__(self):
        super().__init__('FullShoot')
        self.requires(Shooter())

    def initialize(self):
        self.requires(Shooter())
        if Shooter().get_state() == Shooter().State.STOPPED:
            Shooter().set_motors_percentage(1.0)
            Shooter().state = Shooter().State.SPOOLING

    def execute(self):
        
    

    def isFinished(self):
        pass

    def end(self):
        Shooter().set_motors_percentage()

    def interrupted(self):
        pass

