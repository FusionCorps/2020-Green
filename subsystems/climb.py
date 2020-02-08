from wpilib.command import Subsystem
from wpilib import DigitalInput
from ctre import WPI_TalonSRX, ControlMode
from enum import Enum
from fusion.sensors import SensorService, Manager, Report, ReportError
import math

class UltrasoundService()
    
    SENSOR_L_ID = 'C3'
    SENSOR_R_ID = 'C4'
    
    def __init__(self):
        super().__init__("UltrasoundService")

        self._l_sensor = DigitalInput(UltrasoundService.SENSOR_L_ID)
        self._r_sensor = DigitalInput(UltrasoundService.SENSOR_R_ID)

        self.previous_state = (None, None)
        self.current_state = (None, None)

    class UltrasoundReport(Report):
        def __init__(self, service: SensorService):
            super().__init__()

            if service.previous_state == service.current_state:
                raise ReportError("IRService", "No Changes")

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

    @staticmethod
    def where_to_hang_self(sensor_width, m_6672, m_1, m_2, m_bar):
        # Find where to hang robot to balance bar
        report = Manager().get(UltrasoundReport)
        alpha = atan(0.66/1.41)
        theta = atan((report[0] - report[1])/sensor_width)
        distance = 0.66*(report[0] - report[1])*(m_1 + m_2 + m_bar)/(m_6672*sensor_width)
        height = (2.83 - 1.56*sin(alpha + theta) + (1.41 + distance)*sin(theta))
        return height
    
    def turn_ticks(self, ticks:int):
        self.climb_controller.set(ControlMode.MotionMagic, ticks)

    def turn_off(self):
        self.climb_controller.motorOff()

