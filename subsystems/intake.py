import math
from datetime import datetime, timedelta
from threading import RLock, Thread
from time import sleep
from typing import List

from ctre import WPI_TalonFX
from wpilib import SPI
from wpilib.command import Subsystem
from wpilib.drive import DifferentialDrive


class Intake(Subsystem):
    def __init__(self):
        super().__init__("Intake")
