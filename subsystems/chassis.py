"""
Chassis functionality.
"""
import math
from datetime import datetime, timedelta
from threading import RLock, Thread
from time import sleep
from typing import List

from ctre import WPI_TalonSRX
from navx import AHRS

from wpilib import SPI
from wpilib.command import Subsystem
from wpilib.drive import DifferentialDrive
from wpilib import Timer


class JerkSample:
    """
    A sample of the chassis jerk from the navX AHRS sensor.
    """

    def __init__(
        self, x_jerk: float, y_jerk: float, z_jerk: float, collection_time: datetime
    ):
        """
        Construct a JerkSample

        Args:
            x_jerk (float): x-axis jerk
            y_jerk (float): y-axis jerk
            z_jerk (float): z-axis jerk
            collection_time (datetime): the time at which the sample was collected
        """
        self.x_jerk = x_jerk
        self.y_jerk = y_jerk
        self.z_jerk = z_jerk

        self.mag_jerk = math.sqrt(
            math.pow(self.x_jerk, 2)
            + math.pow(self.y_jerk, 2)
            + math.pow(self.z_jerk, 2)
        )

        self.collection_time = collection_time


class Chassis(Subsystem):
    """
    Singleton subsystem containing all driving functionality.
    """

    _instance = (
        None  # Chassis is a singleton. This class attribute stores the only instance.
    )

    TALON_F_R_ID = 1
    TOLON_F_L_ID = 0
    TALON_B_L_ID = 2
    TALON_B_R_ID = 3

    COLLISION_THRESHOLD = 0.5  # G --- Threshold for jerk to be above
    COLLISION_PEAK_TIME = 0.01  # s --- Time above peak before collision is registered
    JERK_POLL_RATE = 0.01  # s --- Sample rate of navX AHRS

    TALON_FPID = (0.0, 1.0, 0.0, 0.0)

    TARGET_VELOCITY = 20000 # Encoder ticks per 100ms
    ACCELERATION = 10000 # Encoder ticks per 100ms per s
    S_CURVE_STRENGTH = 1 # Int from 1 to 8, 1 is trapezoidal, 8 is maximum smooth

    def __new__(cls):
        """
        Python dunder that controls the creation of an instance.
        """

        if cls._instance is None:
            cls._instance = super(Chassis, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        super().__init__("Chassis")

        self._lock = (
            RLock()
        )  # The Lock object allows us to safely modify variables that are shared between Threads

        """
        Speed Controllers
        """
        self._talon_f_r = WPI_TalonFX(Chassis.TALON_F_R_ID)
        self._talon_f_l = WPI_TalonFX(Chassis.TOLON_F_L_ID)
        self._talon_b_l = WPI_TalonFX(Chassis.TALON_B_L_ID)
        self._talon_b_r = WPI_TalonFX(Chassis.TALON_B_R_ID)

        self._left_motors = [self._talon_f_l, self._talon_f_r]
        self._right_motors = [self._talon_b_l, self._talon_b_r]

        for motor in self._left_motors:
            motor.config_kP(Chassis.TALON_FPID[1])
            motor.config_kI(Chassis.TALON_FPID[2])
            motor.config_kD(Chassis.TALON_FPID[3])

            motor.configCruiseVelocity(Chassis.TARGET_VELOCITY)
            motor.configAcceleration(Chassis.ACCELERATION)
            motor.configSCurveStrength(Chassis.S_CURVE_STRENGTH)

        for motor in self._right_motors:
            motor.config_kP(Chassis.TALON_FPID[1])
            motor.config_kI(Chassis.TALON_FPID[2])
            motor.config_kD(Chassis.TALON_FPID[3])

            motor.configCruiseVelocity(Chassis.TARGET_VELOCITY)
            motor.configAcceleration(Chassis.ACCELERATION)
            motor.configSCurveStrength(Chassis.S_CURVE_STRENGTH)

        self._drive = DifferentialDrive(self._left_motors, self._right_motors)

        chassis = Chassis()
