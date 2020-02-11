from ctre import ControlMode
from math import pi
from wpilib.command import Command
from subsystems.indexer import Indexer, IRService
from fusion.sensors import SensorService, Report, ReportError, Manager


class ShiftOverOneSlot(Command):
    BALL_DIAMETER = 0.2  # m
    WHEEL_RADIUS = 0.009525

    REQUIRED_TICKS = BALL_DIAMETER * 2048 / 2 / pi / 0.009525

    def __init__(self):
        super().__init__("ShiftOverOneSlot")

        self.requires(Indexer())

    def initialize(self):
        Indexer().zero_encoder()
        Indexer().set_belt(ControlMode.Position, REQUIRED_TICKS)

    def isFinished(self):
        if Indexer().get_position() == ShiftOverOneSlot.REQUIRED_TICKS:
            return True

    def end(self):
        pass

