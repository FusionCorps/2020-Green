import logging
import multiprocessing as mp
import multiprocessing.queues as mpq
import threading as th
from abc import ABC, ABCMeta, abstractmethod
from array import array
from datetime import datetime, timedelta
from enum import Enum
from inspect import signature
from queue import Empty, Full, Queue
from time import sleep
from typing import Dict, List, Tuple, Type

import wpilib

# from navx import AHRS
# from wpilib import SPI, DigitalInput, Timer


class ReportError(Exception):
    def __init__(self, service: str, msg: str):
        super().__init__()

        self.service = service
        self.msg = msg


class Report(ABC):
    """
    Abstract Base Class that encodes common Report behavior.
    """

    @abstractmethod
    def is_old(self) -> bool:
        """
        Check whether this Report should be flagged for deletion.
        """
        pass


class SensorService(ABC, th.Thread):
    """
    An ABC implementing common functionality shared between Sensor Services.
    """

    def __init__(self):
        super().__init__(target=self._process)

        self._last_poll: datetime = None  # Last sensor update
        self._queue: Queue = Queue(100)
        self._is_killed = th.Event()

    @abstractmethod
    def update(self):
        """
        Defines how the sensors collect data and store it.
        """
        pass

    def _process(self):
        """
        Defines how data is evaluated and Reports are added to queues.
        """
        while True:
            if self._is_killed.is_set():
                return

            self.update()

            for report_class in [
                report_class
                for report_class in type(self).__dict__.values()
                if type(report_class) == ABCMeta and issubclass(report_class, Report)
            ]:
                try:
                    self._queue.put(report_class(self))
                except ReportError:
                    pass

    def _kill(self):
        """
        Common interface for killing services.
        """
        self._is_killed.set()


class Manager(mp.Process):
    """
    A Process that Manages the other Sensors, making sure they are
    called on time. Reports their status to CommandBased robot.
    """

    _services: Dict[Type[SensorService], List[th.Thread]] = None
    _instance = None

    """
    Reports are classes defined within a Service class that implement
    the Report ABC above.
    """
    _reports: Dict[Type[SensorService], List[Report]] = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Manager, cls).__new__(cls)
        return cls._instance

    def __init__(self, services: List[Type[SensorService]]):
        super().__init__(target=self.manage)

        self._services: Dict[Type[SensorService], List[th.Thread]] = {}
        self._reports: Dict[Type[SensorService], List[Report]] = {}

        for s in services:
            self._services[s] = []

        self._logger = logging.getLogger("Manager")
        self._is_killed = mp.Event()
        self._mp_lock = mp.RLock()

    def start_services(self):
        """
        Start threads for all registered services.
        """

        with self._mp_lock:
            for service in self._services.keys():
                try:
                    self._services[service].append(service_thread := service())
                except KeyError:
                    self._services[service] = [service_thread := service()]
                finally:
                    self._reports[service_thread] = []
                    service_thread.start()

    def add_service(self, service: Type[SensorService]):
        """
        Add a new service to be immediately run. If the service exists already,
        add a new instance of that service to the list of running services.
        """
        with self._mp_lock:
            try:
                self._services[service].append(service_thread := service())
            except KeyError:
                self._services[service] = [service_thread := service()]
            finally:
                service_thread.start()

    def _poll_reports(self):
        while True:
            if self._is_killed.is_set():
                self._kill_services()  # Kill all the services before killing self
                return

            with self._mp_lock:  # Use lock to get all the updated Reports
                queues = []

                for service_thread_list in self._services.values():
                    for service in service_thread_list:
                        queues.append((service, service._queue))

            for service, queue in queues:
                while True:
                    try:
                        self._reports[service].append(queue.get_nowait())
                    except Empty:
                        break

    def _cull_reports(self):
        """
        Remove old Reports.
        """
        while True:
            with self._mp_lock:
                for service, report_list in self._reports.items():
                    for report in report_list:
                        if report.is_old():
                            self._reports[service].remove(report)

    def kill(self):
        """
        End the SensorManager and its child Services.
        """
        self._logger.warning("SensorManager is ending...")
        self._is_killed.set()
        self.join()

    def _kill_services(self):
        """
        Kill all Services and reset the threads list.
        """
        with self._mp_lock:
            for service_thread_list in self._services.values():
                for thread in service_thread_list:
                    thread.kill()  # Sets kill event flag to signal service should wrap up
                    thread.join()  # Blocks until service is dead

            for service in self._services.keys():
                self._services[service] = None  # Reset threads to None

    def manage(self):
        self.start_services()
        self._run_loop()

    def _run_loop(self):
        self._poll_reports()

    def get(self, report_type: Type[Report]) -> List[Report]:
        with self._mp_lock:
            return_list = []

            for report_list in self._reports.values():
                for report in report_list:
                    if isinstance(report, report_type):
                        return_list.append(report)

        return return_list


class Tester(SensorService):
    """
    A Dummy service used to test if everything is working.
    """

    class IncreasedByTen(Report):
        def __init__(self, service):
            if service.get_counter() % 10 > 0:
                pass
            else:
                raise ReportError(f"{service.name}", "IncreasedByTen")

            self.created = datetime.now()

        def is_old(self) -> bool:
            return datetime.now() - self.created > timedelta(seconds=1)

    def __init__(self):
        super().__init__()

        self.lock = th.RLock()

        self.counter = 1

    def update(self):
        with self.lock:
            self.counter += 1

        sleep(1)

    def get_counter(self):
        with self.lock:
            return self.counter


def test_manager():
    manager = Manager([Tester])
    manager.start()

    timer = wpilib.Timer()
    timer.start()

    while not timer.hasPeriodPassed(10):
        sleep(1)
        assert len(manager.get(Tester.IncreasedByTen)) > 0


# TODO Move these services into their respective subsystems


# class IndexerService(SensorService):
#     """
#     Sensor Service that detects when IR Light breakage sensors' states
#     change.

#     NOTE: This class is a Singleton.
#     """

#     _instance = None


#     POLL_RATE = 0.002  # s -- Light Breakage poll rate

#     DIO_HALL_SENSOR = 0
#     DIO_BEND_SENSOR = 1
#     DIO_CHUTE_SENSOR = 2

#     class IRSensorState(Enum):
#         UNBROKEN = False
#         BROKEN = True

#     class BallReport(Report):
#         def __init__(
#             self, service: HopperService,
#         ):
#             """
#             Construct a new BallReport. Expires after 100 ms.
#             """
#             self.collection = datetime.now()

#         def is_old(self) -> bool:
#             return datetime.now() - self.collection > timedelta(millis=100)

#     def __new__(cls, *args, **kwargs):
#         if cls._instance is None:
#             cls._instance = super(IndexerService, cls).__new__(cls, *args, **kwargs)
#         return cls._instance

#     def __init__(self):
#         super().__init__()
#         self.hall_sensor = DigitalInput(self.DIO_HALL_SENSOR)
#         self.bend_sensor = DigitalInput(self.DIO_BEND_SENSOR)
#         self.chute_sensor = DigitalInput(self.DIO_CHUTE_SENSOR)

#         self.sensors = [
#             self.hall_sensor,
#             self.bend_sensor,
#             self.chute_sensor,
#         ]

#         self.previous_hall_state: HopperService.IRSensorState = None
#         self.previous_bend_state: HopperService.IRSensorState = None
#         self.previous_chute_state: HopperService.IRSensorState = None

#     def get_hall(self) -> HopperService.IRSensorState:
#         pass

#     def update(self):
#         pass


# class CollisionService(SensorService):
#     """
#     Sensor Service tracking collision events using the NavX AHRS sensor
#     collection.

#     NOTE: This class is a Singleton.
#     """

#     _instance = None

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
#             return datetime.now() - self.collection_time < timedelta(seconds=1)

#     def __new__(cls, *args, **kwargs):
#         if cls._instance is None:
#             cls._instance = super(CollisionService, cls).__new__(cls, *args, **kwargs)

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
#         pass  # TODO
