import logging
import multiprocessing as mp
import multiprocessing.queues as mpq
import threading as th
from abc import ABC, abstractmethod
from array import array
from datetime import datetime, timedelta
from enum import Enum
from inspect import signature
from queue import Queue
from typing import Dict, List, Tuple, Type

from wpilib import DigitalInput

# from navx import AHRS
# from wpilib import SPI, Timer


class ReportError(Enum, Exception):
    INVALID_CRITERIA = "INVALID_CRITERIA"


class Report(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def is_old(self, *args) -> bool:
        """
        Check whether this Report should be flagged for deletion.
        """
        pass


class SensorService(ABC):
    """
    An ABC implementing common functionality shared between Sensor Services.
    """

    def __init__(self, name: str):
        self._last_poll: datetime = None  # Last sensor update
        self._queue: Queue = Queue(max_size=10)

    @abstractmethod
    def update(self):
        """
        Defines how the sensors collect data and store it.
        """
        pass

    def process(self):
        """
        Defines how data is evaluated and Reports are added to queues.
        """
        for report_class in filter(issubclass(Report), type(self).__dict__.values()):
            try:
                report = report_class(self)
                self._queue.put(report)
            except ReportError:
                pass


class SensorManager(mp.Process):
    """
    A Process that Manages the other Sensors, making sure they are
    called on time. Reports their status to CommandBased robot.
    """

    _services: Dict[Type[SensorService], List[th.Thread]] = None
    _instance = None
    _reports: mpq.Queue = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SensorManager, cls).__new__()
        return cls._instance

    def __init__(self, services: List[Type[SensorService]]):
        for s in services:
            self._services[s] = None
        self._reports = mpq.Queue()

    def start_services(self):
        """
        Start threads for all registered services.
        """
        for s, t in self._services.items():
            self._services[s] = (t := s())
            t.start()

    def add_service(self, service: Type[SensorService]):
        """
        Add a service to be run by the Manager.
        """
        self._services[service] = (s := service())
        s.start()

    def kill(self):
        pass


class HopperService(SensorService, th.Thread):
    POLL_RATE = 0.002  # s -- Light Breakage poll rate

    DIO_HALL_SENSOR = 0
    DIO_BEND_SENSOR = 1
    DIO_CHUTE_SENSOR = 2

    class IRSensorState(Enum):
        UNBROKEN = False
        BROKEN = True

    class BallReport(Report):
        def __init__(
            self, service: HopperService,
        ):
            """
            Construct a new BallReport. Expires after 100 ms.
            """
            self.collection = datetime.now()

        def is_old(self) -> bool:
            return datetime.now() - self.collection > timedelta(millis=100)

    def __init__(self):
        self.hall_sensor = DigitalInput(self.DIO_HALL_SENSOR)
        self.bend_sensor = DigitalInput(self.DIO_BEND_SENSOR)
        self.chute_sensor = DigitalInput(self.DIO_CHUTE_SENSOR)

        self.sensors: List[DigitalInput] = [
            self.hall_sensor,
            self.bend_sensor,
            self.chute_sensor,
        ]

        self.previous_hall_state: HopperService.IRSensorState = None
        self.previous_bend_state: HopperService.IRSensorState = None
        self.previous_chute_state: HopperService.IRSensorState = None

    def get_hall(self) -> HopperService.IRSensorState:
        pass


# class CollisionService(SensorService, th.Thread):
#     """
#     Sensor Service tracking collision events using the NavX AHRS sensor
#     collection.
#     """

#     POLL_RATE = 0.01  # s -- Maximum sample rate of AHRS sensor

#     class CollisionReport(Report):
#         COLLISION_THRESHOLD = 0.5  # G -- Threshold for collisions
#         COLLISION_PEAK_TIME = 0.01  # s -- Amt. of time measurements must be above threshold before registering a collision

#         def __init__(self, service: SensorService):
#             super().__init__(self)

#             #  TODO: Collision Detection code goes here
#             for a in service._x_jerk_samples:
#                 pass

#         def is_old(self) -> bool:
#             return (current_time := datetime.now()) - self.collection_time < timedelta(
#                 seconds=1
#             )

#     def __init__(self):
#         super(CollisionService, self).__init__()

#         self._ahrs = AHRS(SPI.Port.kMXP)

#         # Arrays used because samples are ordered and of same type -- faster
#         self._x_jerk_samples: array = array("f")
#         self._y_jerk_samples: array = array("f")
#         self._z_jerk_samples: array = array("f")

#         self._time_jerk_samples: List[datetime] = None

#         self._x_last_acceleration: float = 0.0
#         self._y_last_acceleration: float = 0.0
#         self._z_last_acceleration: float = 0.0

#     def update(self):
#         pass
