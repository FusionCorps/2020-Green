from ctre import VictorSRX, ControlMode
from wpilib.command import Subsystem

class Hopper(Subsystem):

    VICTOR_ID = 14

    HOPPER_FPID = (0.0, 1.0, 0.0, 0.0)
    HOPPER_VEL_ACCEL_CURVE = (20000, 10000, 1)

    def __init__(self):
        self.hopper_controller = VictorSRX(Hopper.VICTOR_ID)
        
        self.hopper_controller.config_kF(Hopper.HOPPER_FPID[0])
        self.hopper_controller.config_kP(Hopper.HOPPER_FPID[1])
        self.hopper_controller.config_kI(Hopper.HOPPER_FPID[2])
        self.hopper_controller.config_kD(Hopper.HOPPER_FPID[3])

        self.hopper_controller.configCruiseVelocity(Hopper.HOPPER_VEL_ACCEL_CURVE[0])
        self.hopper_controller.configAcceleration(Hopper.HOPPER_VEL_ACCEL_CURVE[1])
        self.hopper_controller.configSCurveStrength(Hopper.HOPPER_VEL_ACCEL_CURVE[2])
    
    def set_motor(self, control_mode: ControlMode, value):
        self.hopper_controller.set(control_mode, value)

    def turn_off(self):
        self.hopper_controller.motorOff()

    
