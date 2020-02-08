from ctre import ControlMode
from wpilib.command import InstantCommand, CommandGroup, Command

from subsystems.shooter import Shooter


class ToSpooling(CommandGroup):

    class ToSpoolingScheduler(Scheduler):

    def __init__(self):
        super().__init__("ToSpooling")
        self.requires(Shooter())

        self.previous_state = None

        self.addSequential(SetVelocity(Shooter().target_velocity))

    def initialize(self):
        self.previous_state = Shooter().get_state()

    def execute(self):
        if Shooter()._talon_l.getSelectedSensorVelocity() == Shooter.MAX_VELOCITY:
            pass

    def isFinished(self):
        if Shooter()._talon_l.getSelectedSensorVelocity() == Shooter.MAX_VELOCITY:
            retrun True

    def end(self):
        Shooter().set_state(Shooter.State.WAITING)


class SetVelocity(InstantCommand):
    def __init__(self, velocity: int):
        super().__init__("SetVelocity")
        self.requires(Shooter())

        self.velocity = velocity

    def initialize(self):
        Shooter().set(ControlMode.Velocity, self.velocity)


class SetPercentage(InstantCommand):
    def __init__(self, percentage: float):
        super().__init__("SetPercentage")
        self.requires(Shooter())

        self.percentage = percentage

    def initialize(self):
        Shooter().set(ControlMode.Velocity, self.percentage)
