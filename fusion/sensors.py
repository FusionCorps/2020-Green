import logging
import multiprocessing as mp
import multiprocessing.queues as mpq
import threading as th
from abc import ABC, abstractmethod
from array import array
from datetime import datetime, timedelta
from enum import Enum
from inspect import signature
from queue import Empty, Full, Queue
from typing import Dict, List, Tuple, Type

from navx import AHRS
from wpilib import SPI, DigitalInput, Timer


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
    def is_old(self, *args) -> bool:
        """
        Check whether this Report should be flagged for deletion.
        """
        pass


class SensorService(ABC, th.Thread):
    """
    An ABC implementing common functionality shared between Sensor Services.
    """

    def __init__(self):
        super().__init__(target=self.process)

        self._last_poll: datetime = None  # Last sensor update
        self._queue: Queue = Queue(max_size=100)
        self._is_killed = th.Event()

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
        while True:
            if self._is_killed.is_set():
                return

            for report_class in filter(
                issubclass(Report), type(self).__dict__.values()
            ):
                try:
                    self._queue.put(report_class(self))
                except ReportError:
                    pass

    def kill(self):
        """
        Common interface for killing services.
        """
        self._is_killed.set()


class SensorManager(mp.Process):
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
    _reports: mpq.Queue = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(SensorManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, services: List[Type[SensorService]]):
        super().__init__(target=self.begin_managing)

        for s in services:
            self._services[s] = None

        self._reports = mpq.Queue(maxsize=1000)  # Arbitrary limit
        self._logger = logging.getLogger("SensorManager")
        self._is_killed = mpq.Event()
        self._mpq_lock = mpq.RLock()

    def start_services(self):
        """
        Start threads for all registered services.
        """
        for s, t in self._services.items():
            try:
                self._services[s].append(service_thread := s())
            except KeyError:
                self._services[s] = [service_thread := s()]
            finally:
                service_thread.start()

    def add_service(self, service: Type[SensorService]):
        """
        Add a new service to be immediately run. If the service exists already,
        add a new instance of that service to the list of running services.
        """
        with self._mpq_lock:
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

            with self._mpq_lock:
                queues = [
                    queue
                    for queue in (service._queue for service in self._services.values())
                ]

            for q in queues:
                while True:
                    try:
                        self._reports.put(q.get_nowait())
                    except Empty:
                        break
                    except Full:
                        self._logger.error(
                            f"Manager Queue has exceeded its item limit of {self._queue.maxsize}!"
                            f"Removing items until space has cleared: {str(self._reports.get())}!"
                        )

    def kill(self):
        """
        End the SensorManager and its child Services.
        """
        self._is_killed.set()

    def _kill_services(self):
        with self._mpq_lock:
            for service in self._services.values():
                service.kill()  # Sets kill event flag to signal service should wrap up
                service.join()  # Blocks until service is dead

    def begin_managing(self):
        self.start_services()
        self._run_loop()

    def _run_loop(self):
        self._poll_reports()


class TestService(SensorService):
    """
    A Dummy service used to test if everything is working.
    """

    class IncreasedByTenReport(Report):
        def __init__(self, service: TestService):
            super().__init__()

            if service.get_counter() % 10 > 0:
                pass
            else:
                raise ReportError(f"{service.name}", "IncreasedByTen")

            self.created = datetime.now()

        def is_old(self) -> bool:
            return datetime.now() - self.created > timedelta(seconds=1)

    def __init__(self):
        super(TestService, self).__init__()
        super().__init__(target=(self.add_one))

        self.lock = th.RLock()

        self.counter = 1

    def add_one(self):
        with self.lock:
            self.counter += 1

    def get_counter(self):
        with self.lock:
            return self.counter


# TODO Move these services into their respective subsystems


class IndexerService(SensorService):
    """
    Sensor Service that detects when IR Light breakage sensors' states
    change.

    NOTE: This class is a Singleton.
    """

    _instance = None

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

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(IndexerService, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        super().__init__()
        self.hall_sensor = DigitalInput(self.DIO_HALL_SENSOR)
        self.bend_sensor = DigitalInput(self.DIO_BEND_SENSOR)
        self.chute_sensor = DigitalInput(self.DIO_CHUTE_SENSOR)

        self.sensors = [
            self.hall_sensor,
            self.bend_sensor,
            self.chute_sensor,
        ]

        self.previous_hall_state: HopperService.IRSensorState = None
        self.previous_bend_state: HopperService.IRSensorState = None
        self.previous_chute_state: HopperService.IRSensorState = None

    def get_hall(self) -> HopperService.IRSensorState:
        pass

    def update(self):
        pass


class CollisionService(SensorService):
    """
    Sensor Service tracking collision events using the NavX AHRS sensor
    collection.

    NOTE: This class is a Singleton.
    """

    _instance = None

    POLL_RATE = 0.01  # s -- Maximum sample rate of AHRS sensor

    class CollisionReport(Report):
        COLLISION_THRESHOLD = 0.5  # G -- Threshold for collisions
        COLLISION_PEAK_TIME = 0.01  # s -- Amt. of time measurements must be above threshold before registering a collision

        def __init__(self, service: SensorService):
            super().__init__(self)

            #  TODO: Collision Detection code goes here
            for a in service._x_jerk_samples:
                pass

        def is_old(self) -> bool:
            return datetime.now() - self.collection_time < timedelta(seconds=1)

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(CollisionService, cls).__new__(cls, *args, **kwargs)

    def __init__(self):
        super(CollisionService, self).__init__()

        self._ahrs = AHRS(SPI.Port.kMXP)

        # Arrays used because samples are ordered and of same type -- faster
        self._x_jerk_samples: array = array("f")
        self._y_jerk_samples: array = array("f")
        self._z_jerk_samples: array = array("f")

        self._time_jerk_samples: List[datetime] = None

        self._x_last_acceleration: float = 0.0
        self._y_last_acceleration: float = 0.0
        self._z_last_acceleration: float = 0.0

    def update(self):
        pass  # TODO
