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

    PID_P = 1.0
    PIP_I = 0.0
    PIP_D = 0.0

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

        self._left_motors.config_kP(Chassis.PID_P)
        self._left_motors.config_kI(Chassis.PIP_I)
        self._left_motors.config_kD(Chassis.PIP_D)

        self._left_motors.configCruiseVelocity(Chassis.TARGET_VELOCITY)
        self._left_motors.configAcceleration(Chassis.ACCELERATION)
        self._left_motors.configSCurveStrength(Chassis.S_CURVE_STRENGTH)

        self._right_motors.config_kP(Chassis.PID_P)
        self._right_motors.config_kI(Chassis.PIP_I)
        self._right_motors.config_kD(Chassis.PIP_D)

        self._right_motors.configCruiseVelocity(Chassis.TARGET_VELOCITY)
        self._right_motors.configAcceleration(Chassis.ACCELERATION)
        self._right_motors.configSCurveStrength(Chassis.S_CURVE_STRENGTH)

        self._drive = DifferentialDrive(self._left_motors, self._right_motors)

        """
        Collision Detection
        """
        self._timer = Timer()
        self._ahrs = AHRS(SPI.Port.kMXP)

        self._jerk_last_poll = datetime.now()
        self._jerk_samples: List[JerkSample] = []

        self._has_collided = False
        self._block_triggered = False
        self.block_count = 0

        self._collisions = (
            []
        )  # Contains list of tuples with (<magnitude of collision jerk>, <collision time>)

        self._last_x_accel = 0.0
        self._last_y_accel = 0.0
        self._last_z_accel = 0.0

        self._collision_detector = Thread(target=self._update_collisions)
        self._collision_detector.start()  # Runs collision detection in a separate thread

    def joystick_drive(self, x_axis: int, y_axis: int) -> None:
        self._drive.curvatureDrive(x_axis, y_axis, True)

    def set_motors_ticks(l_ticks: int, r_ticks: int):
        self._left_motors.set(ControlMode.MotionMagic, l_ticks)
        self._right_motors.set(ControlMode.MotionMagic, r_ticks)

    def set_motors_velocity(l_velocity: int, r_velocity: int):
        self._left_motors.set(ControlMode.Velocity, l_velocity)
        self._right_motors.set(ControlMode.Velocity, r_velocity)
    @staticmethod
    def calculate_jerk(
        accel_last: float, accel_curr: float, tm_diff: timedelta
    ) -> float:
        """
        Calculate jerk given a difference in acceleration and a timedelta

        Args:
            accel_last (float): previous acceleration
            accel_curr (float): new acceleration
            tm_diff (timedelta): time between the measurement of the last and new acceleration

        Returns:
            float: jerk in Gs
        """

        try:
            return abs(accel_last - accel_curr) / tm_diff.total_seconds()
        except ZeroDivisionError:
            return 0.0

    @property
    def collided(self) -> bool:
        """
        Whether the chassis has detected a collision recently or not

        Returns:
            bool: whether a collision has occurred
        """

        with self._lock:
            return self._has_collided

    def _update_collisions(self) -> None:
        with self._lock:
            self._poll_jerk()

            for i in range(len(self._jerk_samples)):
                try:
                    
                    self._block_time = 0
                    self._block_size = 0
                    while self._block_time < self.JERK_POLL_RATE:
                        self._block_time = self._jerk_samples[-i].collection_time - self._jerk_samples[-i - self._block_size].collection_time
                        self._block_size += 1
                    if self._jerk_samples[-i].collection_time - self._jerk_samples[-i - self._block_size].collection_time> timedelta(
                        seconds=Chassis.COLLISION_PEAK_TIME
                    )   :  # Measurement time from sample to sample must be above the PEAK_TIME constant
                        self._block_triggered = all(
                            map(
                                lambda j: j.mag_jerk > Chassis.COLLISION_THRESHOLD,
                                self._jerk_samples[-i - 2 :],
                            )
                        )  # Sets collision flag to whether all the jerk samples are above the threshold
                        
                        self.block_count += 1

                        if self.block_count > 3:
                            self._has_collided = True
                        else:
                            self.block_count -= 2
                        
                        if self._has_collided:
                            self._timer.start()

                        if self._timer.hasPeriodPassed(0.02):
                            self._has_collided = False
                            self._timer.reset()

                            break  # Breaks before searching whole sample list unnecessarily
                        

                except IndexError:
                    self._has_collided = False

                   

        sleep(Chassis.JERK_POLL_RATE)  # Allows main thread to read from variables

    def _poll_jerk(self) -> None:
        elapsed_time = (curr_time := datetime.now()) - self._jerk_samples[
            -1
        ].collection_time  # timedelta since last poll

        self._jerk_samples = list(
            filter(
                lambda j: datetime.now() - j.collection_time < timedelta(seconds=1),
                self._jerk_samples,
            )
        )  # Throw out any samples older than 1 second

        self._jerk_samples.append(
            JerkSample(
                Chassis.calculate_jerk(
                    self._last_x_accel,
                    curr_x_accel := self._ahrs.getWorldLinearAccelX(),
                    elapsed_time,
                ),
                Chassis.calculate_jerk(
                    self._last_y_accel,
                    curr_y_accel := self._ahrs.getWorldLinearAccelY(),
                    elapsed_time,
                ),
                Chassis.calculate_jerk(
                    self._last_z_accel,
                    curr_z_accel := self._ahrs.getWorldLinearAccelZ(),
                    elapsed_time,
                ),
                curr_time,
            )
        )  # Add the new jerk samples

        self._last_x_accel = curr_x_accel
        self._last_y_accel = curr_y_accel
        self._last_z_accel = curr_z_accel
