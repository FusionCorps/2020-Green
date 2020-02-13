from subsystems.climb import Climb
from wpilib.command import Command
from ctre import ControlMode

class Extend(Command):

    def __init__(self):
        super().__init__('Climb')
        self.requires(Climb())

    def initialize(self):
        return super().initialize(name="Extend", timeout=0.0, subsystem=Climb)
        if Climb().state == Climb.ClimbState.LOWERED:
            Climb().set_speed_motor(ControlMode.MotionMagic, Climb.TICKS_TO_FULL)
            Climb().state == Climb.ClimbState.RISING
        
    
    def isFinished(self):
        if Climb().get_speed_motor() == 19456:
            return True

    def end(self):
        Climb().state = Climb.ClimbState.RAISED

            

