from wpilib.command import InstantCommand 
from subsystems import hopper
from ctre import ControlMode

class SetHopper(InstantCommand):
    def __init__(self, control_mode: ControlMode, value):
        super().__init__('SetHopper')
        self.value = value
        self.requires(hopper)
        self.control_mode = control_mode
    
    def initialize(self):
        hopper.set_motor(self.control_mode, self.value)
    

