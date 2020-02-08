from itertools import islice
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
from navx import AHRS
from wpilib import SPI, DigitalInput, Timer


class ReportError(Exception):
    """An Exception that indicates a Report cannot be generated.

    An Exception used to indicate that a Report cannot
    be generated, usually because of insufficient information
    or because the provided values do not satisfy the
    reporting criteria.

    Args:
        service (str): The service that generated the Exception
        msg (str): Human-readable string describing the Exception

    Attributes:
        service (str): The service that generated the Exception
        msg (str): Human-readable string describing the Exception

    Note:
        ReportError Exceptions should be raised in the __init__
        method of a Report when that Report is not ready to be
        generated.
    """

    def __init__(self, service: str, msg: str):
        super().__init__()

        self.service = service
        self.msg = msg


class Report(ABC):
    """Object that encodes essential information into an event.

    Abstract Base Class that encodes common Report behavior.

    """

    @abstractmethod
    def is_old(self) -> bool:
        """Check whether this Report should be flagged for deletion.

        Returns:
            bool: Whether this Report has expired and should be deleted.
        """
        pass


class Service(ABC, th.Thread):
    """A sensor or collection of sensors that share a common purpose.

    A SensorService is a Thread that is managed and run by the `SensorManager`.

    Note:
        Each service must be registered with the `SensorManager` before
        they are run.
    """

    def __init__(self, poll_rate: float):
        super().__init__(target=self._process)

        self._last_poll: datetime = None  # Last sensor update
        self._poll_rate = poll_rate

        self._queue: Queue = Queue(100)  # Arbitrary limit of 100 elements
        self._is_killed = th.Event()  # If set, Service will be terminated ASAP

    @abstractmethod
    def update(self):
        """Defines how new data should be collected and stored from sensor(s).

        This method is automatically called by the `SensorManager`. All
        repeating update steps should be contained here.
        """
        pass

    def _process(self):
        """An internal method that checks for Reports and adds them if
        possible.
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

            sleep(self._poll_rate)

    def _kill(self):
        """
        Common interface for killing services.
        """
        self._is_killed.set()


class Manager(mp.Process):
    """Manages other Services by updating data and aggregating Reports.

    A Process that Manages the other Sensors, making sure they are
    called on time. Reports their status to CommandBased robot.

    Args:
        services (List[Type[Service]]): A list of the Service classes
            that will be registered from the start.

    Note:
        `Manager` is a Singleton.
    """

    _instance = None  # Holds Manager instance, queue, and kill flag in tuple
    _queue: mpq.Queue = None
    _killed: mp.Event = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Manager, cls).__new__(cls)
        return cls._instance

    def __init__(self, services: Optional[List[SensorService]] = None):
        super().__init__(target=self.manage)

        self._services: Dict[Type[Service], List[th.Thread]] = {}
        self._reports: Dict[Type[Service], List[Report]] = {}

        if services is None:
            raise ValueError("`services` cannot be None!")

        for service in services:
            self._services[service] = []

        Manager._queue = mpq.Queue(1000)
        Manager._killed = mp.Event()

        self._logger = logging.getLogger("Manager")

    def _start_services(self):
        """
        Start threads for all registered services.
        """

        for service in self._services.keys():
            try:
                self._services[service].append(service_thread := service())
            except KeyError:
                self._services[service] = [service_thread := service()]
            finally:
                self._reports[service_thread] = []
                service_thread.start()

    def _poll_reports(self):
        while True:
            if Manager._killed.is_set():
                self._kill_services()  # Kill all the services before killing self
                return

            queues = []

            for service_thread_list in self._services.values():
                for service in service_thread_list:
                    queues.append((service, service._queue))

            for service, queue in queues:
                while True:
                    try:
                        self._reports[service].append(queue.get())
                    except Empty:
                        break

    def _cull_reports(self):
        """
        Remove old Reports.
        """
        while True:
            for service, report_list in self._reports.items():
                for report in report_list:
                    if report.is_old():
                        self._reports[service].remove(report)

    def kill(self):
        """
        End the SensorManager and its child Services.
        """

        self._logger.warning("SensorManager is ending...")
        Manager._killed.set()
        Manager().join()

    def _kill_services(self):
        """
        Kill all Services and reset the threads list.
        """

        for service_thread_list in self._services.values():
            for thread in service_thread_list:
                thread.kill()  # Sets kill event flag to signal service should wrap up
                thread.join()  # Blocks until service is dead

        for service in self._services.keys():
            self._services[service] = None  # Reset threads to None

    def manage(self):
        self._start_services()
        self._poll_reports()


class Client(th.Thread):
    _instance = None
    _reports: List[Report] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Client, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        super().__init__(target=self._update_reports)

        self.lock = th.RLock()

    def _update_reports(self):
        while True:
            with self.lock:
                for r in Client._reports:
                    if r.is_old():
                        Client._reports.remove(r)

                try:
                    Client._reports.append(Manager()._queue.get())
                except Empty:
                    break

    def get(self, report: Type[Report], number: int = -1) -> List[Report]:
        with self.lock:
            return [r for r in Client._reports if type(r) == report][:-number]


class Tester(Service):
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

