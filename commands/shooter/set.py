from ctre import ControlMode
from wpilib.command import InstantCommand, CommandGroup, Command

from subsystems.shooter import Shooter


class Wait(CommandGroup):
    def __init__(self):
        super().__init__("Wait")

        self.requires(Shooter())

    def initialize(self):
        pass

    def execute(self):
        pass

    def isFinished(self):
        return False

    def end(self):
        pass


class Spool(CommandGroup):
    """Bring the Shooter up to speed.
    """

    def __init__(self):
        super().__init__("Spooling")

        self.requires(Shooter())

        self.addSequential(SetVelocity(Shooter.MAX_VELOCITY))

    def initialize(self):
        self.previous_state = Shooter().get_state()

    def execute(self):
        pass

    def isFinished(self):
        return Shooter().get_velocity() >= Shooter.MAX_VELOCITY

    def end(self):
        Wait().start()


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
