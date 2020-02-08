from wpilib.command import InstantCommand 
from subsystems.hopper import Hopper

class SetHopper(InstantCommand):
    def __init__(self, velocity):
        super().__init__('SetHopper')
        self.velocity = velocity
        self.requires(Hopper())
    
    def initialize(self):
        Hopper().set_motor_velocity(self.velocity)
    

