from subsystems.shooter import Shooter
from wpilib.command import Command
from subsystems import shooter


class FullShoot(Command):

    def __init__(self):
        super().__init__('FullShoot')
        self.requires(shooter)

    def initialize(self):
        self.requires(shooter)
        if shooter.get_state() == shooter.State.STOPPED:
            shooter.set_motors_percentage(1.0)
            shooter.state = shooter.State.SPOOLING

    def execute(self):
        pass

    def isFinished(self):
        pass

    def end(self):
        shooter.set_motors_percentage()

    def interrupted(self):
        pass

