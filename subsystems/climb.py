from wpilib.command import Subsystem
from fusion.sensors import SensorService, Report, ReportError, Manager
from wpilib import DigitalInput

class UltrasoundService(SensorService):
    
    POLL_RATE = 0.1 # s
    





class Climb(Subsystem):
    def __init__(self):

        