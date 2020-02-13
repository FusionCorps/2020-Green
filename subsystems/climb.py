from wpilib.command import Subsystem
from wpilib import DigitalInput
from ctre import WPI_TalonFX, ControlMode
from enum import Enum
from fusion.sensors import SensorService, Manager, Report, ReportError
import math

class UltrasoundService():
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

    TICKS_TO_FULL = 19456 # ticks

    class ClimbState(Enum):
        LOWERED = 0
        RAISED = 1
        RISING = 2
        LOWERING = 3
        LIFTING = 4 # Lowering while lifting the robot up

    def __init__(self):
        self.climb_speed = WPI_TalonFX(Climb.TALON_ID)
        self.state = Climb.ClimbState.LOWERED
        self.climb_power = WPI_TalonFX(Climb.TALON_ID)

        for climb_controller in [self.climb_speed, self.climb_power]:
            climb_controller.config_kP(Climb.CLIMB_P)
            climb_controller.config_kI(Climb.CLIMB_I)
            climb_controller.config_kD(Climb.CLIMB_D)
            climb_controller.configAcceleration(Climb.ACCEL)
            climb_controller.configCruiseVelocity(Climb.DEFAULT_SPEED)
            climb_controller.configSCurveStrength(Climb.S_CURVE_STRENGTH)
            
            climb_controller.setSelectedSensorValue(0) # Zero

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
    
    def set_speed_motor(self, mode: ControlMode, value):
        self.climb_speed.set(mode, value)

    def set_power_motor(self, mode: ControlMode, value):
        self.climb_power.set(mode, value)
    
    def get_speed_motor(self):
        return self.climb_speed.get()

    def get_power_motor(self):
        return self.climb_power.get()

    def turn_off_power(self):
        self.climb_power.motorOff()

    def turn_off_speed(self):
        self.climb_speed.motorOff()

