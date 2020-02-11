from wpilib.command import InstantCommand
from subsystems.chassis import Chassis
from pynetworktables import NetworkTables
from math import pi

class TurnToTarget(InstantCommand):
    def __init__(self):
        super().__init__('TurnToTarget')
        self.requires(Chassis())

    def initialize(self):
        theta = NetworkTables().getTable('limelight').getNumber('tx')
        alpha = 0.2921/0.1024*theta/pi*1024
        Chassis().set_motors_ticks(alpha, -alpha)





