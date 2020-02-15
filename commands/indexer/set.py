from typing import Union

from ctre import ControlMode
from wpilib.command import InstantCommand

from fusion.unique import unique
from subsystems import Indexer


@unique
class IndexerSet(InstantCommand):
    def __init__(self, control_mode: ControlMode, value: Union[float, int]):
        super().__init__(name="IndexerSet")

        self.requires(Indexer())

        self.control_mode = control_mode
        self.value = value

    def initialize(self):
        Indexer().set(self.control_mode, self.value)

