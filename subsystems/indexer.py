from time import sleep
from wpilib.command import Subsystem
from enum import Enum
from ctre import WPI_TalonFX, TalonFXControlMode
from wpilib import DigitalInput
from typing import Optional
from fusion.sensors import SensorService, Report, ReportError, Manager


class IRService(SensorService):
    POLL_RATE = 0.002  # s

    ENTRY_BEND_BEAM_ID = "D1"
    BOTTOM_BEND_BEAM_ID = "D2"
    TOP_BEAM_ID = "D3"
    EXIT_BEAM_ID = "D4"

    class BreakReport(Report):
        def __init__(self, service: SensorService):
            super().__init__()

            if service.previous_state == service.state:
                raise ReportError("IRService", "No Changes")

            self.previous_state = service.previous_state
            self.state = service.state

    def __init__(self):
        self._exit_beam = DigitalInput(IRService.EXIT_BEAM_ID)
        self._top_beam = DigitalInput(IRService.TOP_BEAM_ID)
        self._bottom_beam = DigitalInput(IRService.BOTTOM_BEAM_ID)
        self._entry_beam = DigitalInput(IRService.ENTRY_BEND_BEAM_ID)

        self.state_current = (
            None,
            None,
            None,
            None
        )
        self.state_previous = (
            None,
            None,
            None,
            None
        )

    def update(self):
        self.state_previous = self.state_current
        self.state_current = (
            self._exit_beam.get(),
            self._top_beam.get(),
            self._bottom_beam.get(),
            self._entry_beam.get()
        )


class Indexer(Subsystem):
    _instance = None

    MAX_SPEED = 5  # m/s
    TALON_ID = 11

    class IndexerSpace(Enum):
        FULL = (True, True, True)
        EMPTY = (False, False, False)
        HORIZONTAL = (False, True, False)
        VERTICAL = (True, False, False)
        BOTH = (True, True, False)
        ONE = (False, True, True)

    class BallState(Enum):
        ENTERING = 0
        BOTTOM_CORNER = 1
        IN_CORNER = 2
        VERTICAL_CORNER = 3
        UNBUFFERED = 4
        TOP = 5
        SHOOTING = 6

    class FakeBall:
        def __init__(self):
            self.state = Indexer.BallState.ENTERING

        def change_state(self, new_state):
            self.state = new_state

        def return_state(self):
            return self.state

    """
    Defines the motor IDs, beam IDs, and the State Enums for use later
    """

    def __init__(self):
        self.ball_count = 0

        self.belt_controller = WPI_TalonFX(Indexer.TALON_ID)

        self.ball_list = []

        """
        Define all the break beams and motor controllers
        Set the vertical ball count to 0
        """

    @staticmethod
    def convert_ms_to_ticks(self, value: float) -> int:
        pass

    def checkTop(self):
        report = Manager().get(IRService.BreakReport)
        return report[2]

    def setBelt(self, velocity: float = 0):
        # Velocity is in encoder ticks per 100 ms
        self.belt_controller.set(TalonFXControlMode.velocity, velocity)

    def __init__(self):
        super().__init__("IRService", IRService.POLL_RATE)

        self._entry_sensor = DigitalInput(IRService.HORIZ_BEND_BEAM_ID)
        self._bottom_sensor = DigitalInput(IRService.BOTTOM_BEAM_ID)
        self._top_sensor = DigitalInput(IRService.TOP_BEAM_ID)
        self._exit_sensor = DigitalInput(IRService.VERT_BEND_BEAM_ID)

        self.previous_state = (None, None, None, None)
        self.current_state = (None, None, None, None)

    def update(self):
        self.previous_state = self.current_state
        self.current_state = (
            self._entry_sensor.get(),
            self._bottom_sensor.get(),
            self._top_sensor.get(),
            self._exit_sensor.get(),
        )
