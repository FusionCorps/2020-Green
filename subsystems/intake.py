from ctre import VictorSPX, ControlMode
from wpilib.command import Subsystem

class Intake(Subsystem):

    VICTOR_ID = 9

    def __init__(self):
        self.intake_controller = VictorSPX(Intake.VICTOR_ID)
    
    def set_intake(self, velocity:float):
        # Velocity is in ticks/100ms
        self.intake_controller.set(ControlMode.Velocity, velocity)

    def turn_off(self):
        self.intake_controller.stopMotor()



