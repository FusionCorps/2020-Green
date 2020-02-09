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


class Chassis(Subsystem):
    """
    Singleton subsystem containing all driving functionality.
    """

    _instance = None

    # Controller IDs listed counter-clockwise
    TALON_F_R_ID = 1
    TALON_F_L_ID = 0
    TALON_B_L_ID = 2
    TALON_B_R_ID = 3

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Chassis, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        super().__init__("Chassis")

        """
        Speed Controllers
        """
        self._talon_f_r = WPI_TalonSRX(Chassis.TALON_F_R_ID)
        self._talon_f_l = WPI_TalonSRX(Chassis.TALON_F_L_ID)
        self._talon_b_l = WPI_TalonSRX(Chassis.TALON_B_L_ID)
        self._talon_b_r = WPI_TalonSRX(Chassis.TALON_B_R_ID)

        self._left_motors = [self._talon_f_l, self._talon_f_r]
        self._right_motors = [self._talon_b_l, self._talon_b_r]

        self._drive = DifferentialDrive(self._left_motors, self._right_motors)

    def joystick_drive(self, x_axis: int, y_axis: int) -> None:
        """Drive the Chassis using joystick input.

        Sets the DifferentialDrive object's speed using the
        provided joystick inputs.

        Args:
            x_axis (int): Value for the magnitude of the movement
            y_axis (int): Value for the rotation of the movement
        """
        self._drive.curvatureDrive(x_axis, y_axis, True)

    def initDefaultCommand(self):
        from commands.chassis.joystick_drive import JoystickDrive

        self.setDefaultCommand(JoystickDrive)

