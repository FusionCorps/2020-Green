from ctre import VictorSRX, ControlMode
from wpilib.command import Subsystem

class Hopper(Subsystem):

    VICTOR_ID = 14

    def __init__(self):
        
        self.hopper_controller = VictorSRX(Hopper.VICTOR_ID)
    
    def set_motor_velocity(self, velocity):
        self.hopper_controller.set(ControlMode.Velocity, velocity)

    def turn_off(self):
        self.hopper_controller.motorOff()

    
