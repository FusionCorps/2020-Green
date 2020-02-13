from wpilib.command import InstantCommand 
from subsystems.hopper import Hopper
from ctre import ControlMode

class SetHopper(InstantCommand):
    def __init__(self, control_mode: ControlMode, value):
        super().__init__('SetHopper')
        self.value = value
        self.requires(Hopper())
        self.control_mode = control_mode
    
    def initialize(self):
        Hopper().set_motor(self.control_mode, self.value)
    

