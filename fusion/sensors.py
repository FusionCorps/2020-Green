import multiprocessing as mp
import multiprocessing.queues as mpq
import queue as q
import threading as th
from enum import Enum
from typing import List

from navx import AHRS


class ServiceStatus(Enum):
    ACTIVE = "ACTIVE"
    STOPPED = "STOPPED"


class SensorService:
    def __init__(self):
        super().__init__()

        self.status = ServiceStatus.STOPPED



class CollisionDetection(th.Thread, SensorService):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CollisionDetection, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        super(CollisionDetection, self).__init__()

        self._ahrs = AHRS()


class BallDetection(th.Thread, SensorService):
    pass


class SensorDaemon(mp.Process):
    _threads: List[th.Thread] = None
    _lock = th.RLock()

    def __init__(self):
        super().__init__(group, target, name, args, kwargs, *, daemon)

    def register(self, thread: th.Thread):
        """Add a Thread to be run by the SensorService.
        
        Args:
            thread (th.Thread): The target Thread
        """
        if self._threads is None:
            self._threads = [thread]
        else:
            self._threads.append(thread)

    def start_services(self):
        for s in self._threads:
            if not s.isAlive():
                s.start()

