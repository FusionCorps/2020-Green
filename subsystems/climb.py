from wpilib.command import Subsystem
from ctre import WPI_TalonSRX, ControlMode
from enum import Enum

class Climb(Subsystem):

    TALON_ID = 14 

    DEFAULT_SPEED = 10000 # encoder ticks per 100 ms
    ACCEL = 2000 # encode ticks per 100 ms per s
    S_CURVE_STRENGTH = 1 # Int between 1 and 8, with 1 being trapezoidal, and 8 being maximum smooth

    CLIMB_P = 1.0
    CLIMB_I = 0.0
    CLIMB_D = 0.0

    class ClimbState(Enum):
        LOWERED = 0
        RAISED = 1
        RISING = 2
        LOWERING = 3
        LIFTING = 4 # Lowering while lifting the robot up

    def __init__(self):
        self.climb_controller = WPI_TalonSRX(Climb.TALON_ID)
        self.state = Climb.ClimbState.LOWERED

        self.climb_controller.config_kP(Climb.CLIMB_P)
        self.climb_controller.config_kI(Climb.CLIMB_I)
        self.climb_controller.config_kD(Climb.CLIMB_D)
        self.climb_controller.configAcceleration(Climb.ACCEL)
        self.climb_controller.configCruiseVelocity(Climb.DEFAULT_SPEED)
        self.climb_controller.configSCurveStrength(Climb.S_CURVE_STRENGTH)

        # TODO : Add feed-forward looping

    @staticmethod
    def meters_to_ticks(meters):
        # Convert from meters of height to ticks of rotation
        pass
    
    
    def turn_ticks(self, ticks:int):
        self.climb_controller.set(ControlMode.MotionMagic, ticks)

    def turn_off(self):
        self.climb_controller.motorOff()

