from wpilib.command import Subsystem
from wpilib.drive import DifferentialDrive
from rev import CANSparkMax, MotorType
from ctre import WPI_TalonSRX
from wpilib import SPI
from navx import AHRS
import math

class Chassis(Subsystem):
    TALON_FL_PORT = 0
    TALON_FR_PORT = 1
    TALON_BL_PORT = 2
    TALON_BR_PORT = 3
    K_COLLISION_THRESHOLD_DELTA_G = 0.5

    def __init__(self,spd_x,spd_z=0.0,time=None):
        super().__init__("Chassis")
        self.talon_f_l = WPI_TalonSRX(Chassis.TALON_FL_PORT)
        self.talon_f_r = WPI_TalonSRX(Chassis.TALON_FR_PORT)
        self.talon_b_l = WPI_TalonSRX(Chassis.TALON_BL_PORT)
        self.talon_b_r = WPI_TalonSRX(Chassis.TALON_BR_PORT)
        self.left_motors = [self.talon_f_l,self.talon_f_r]
        self.right_motors = [self.talon_b_l,self.talon_b_r]
        self.drive = DifferentialDrive(self.left_motors, self.right_motors)  

        self.collision_timer = 0
        self.ahrs = AHRS(SPI.Port.kMXP)
        self.collision_detected = False
        
        self.last_world_linear_accel_x = 0
        self.last_world_linear_accel_y = 0
        self.last_world_linear_accel_z = 0
        
    def joystick_drive(self, x_axis: int, y_axis: int) -> None:
        self.drive.curvatureDrive(x_axis, y_axis, True)
    
    def collision_detection(self):
        curr_world_linear_accel_x = self.ahrs.getWorldLinearAccelX()
        self.last_world_linear_accel_x = curr_world_linear_accel_x
        currentJerkX = curr_world_linear_accel_x - self.last_world_linear_accel_x
        
        curr_world_linear_accel_y = self.ahrs.getWorldLinearAccelY()
        self.last_world_linear_accel_y = curr_world_linear_accel_y
        currentJerkY = curr_world_linear_accel_y - self.last_world_linear_accel_y
        
        curr_world_linear_accel_z = self.ahrs.getWorldLinearAccelZ()
        self.last_world_linear_accel_z = curr_world_linear_accel_z
        currentJerkZ = curr_world_linear_accel_z - self.last_world_linear_accel_z

        magnitudeJerk = math.sqrt((currentJerkZ**2 + currentJerkY**2 + currentJerkX**2))

        self.collision_timer -= 1

        if magnitudeJerk >  Chassis.K_COLLISION_THRESHOLD_DELTA_G: 
            self.collision_detected = True
            self.collision_timer = 3

        if self.collision_timer <= 0:
            self.collision_detected = False
    
        



        




