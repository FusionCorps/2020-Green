from ctre import ControlMode
from wpilib.command import InstantCommand, CommandGroup, Command, Scheduler
from commands.shooter.shoot import Shoot
from subsystems.shooter import Shooter, Indexer
from subsystems.indexer import IRService
from fusion.sensors import Manager


class ToSpooling(CommandGroup):

    def __init__(self):
        super().__init__("ToSpooling")
        self.requires(Shooter())

        self.previous_state = None

        self.addSequential(SetVelocity(Shooter().target_velocity))

    def initialize(self):
        self.previous_state = Shooter().get_state()
        Shooter().set_state(Shooter.State.SPOOLING)

    def execute(self):
        if Shooter()._talon_l.getSelectedSensorVelocity() == Shooter().target_velocity:
            pass

    def isFinished(self):
        if Shooter()._talon_l.getSelectedSensorVelocity() == Shooter().target_velocity:
            return True

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

class ToShooting(CommandGroup):

    def __init__(self):
        super().__init__('ToShooting')
        self.requires(Shooter())

        self.previous_state = None

        if Indexer().get_state() == Indexer.State.WAITING:
            self.addSequential(Shoot())

    def initialize(self):
        self.previous_state = Shooter().get_state()
        if Indexer().get_state() == Indexer.State.WAITING:
            Shooter().set_state(Shooter.State.SHOOTING)

    def isFinished(self):
        if Manager().get(IRService.BreakReport)[3]:
            return True
    
    def end(self):
        Shooter().set_state(Shooter.State.SPOOLING)

class SetDeltaPosition(InstantCommand):
    def __init__(self, delta_pos):
        super().__init__('SetDelta')
        self.requires(Shooter())
        self.dp = delta_pos

    def initialize(self):
        target_pos = Shooter().get() + self.dp
        Shooter().set(ControlMode.MotionMagic, target_pos)


    


