from subsystems import climb
from wpilib.command import Command
from ctre import ControlMode

class Extend(Command):

    def __init__(self):
        super().__init__('Climb')
        self.requires(climb)

    def initialize(self):
        return super().initialize(name="Extend", timeout=0.0, subsystem=Climb)
        if climb.state == Climb.ClimbState.LOWERED:
            climb.set_extend_motor(ControlMode.MotionMagic, Climb.TICKS_TO_FULL)
            climb.state == Climb.ClimbState.RISING
        
    
    def isFinished(self):
        if climb.get_extend_motor() == 19456:
            return True

    def end(self):
        climb.state = Climb.ClimbState.RAISED

            

