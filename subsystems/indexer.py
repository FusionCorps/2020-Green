from enum import Enum
from time import sleep
from typing import Optional, List

import ctre
from ctre import ControlMode, WPI_TalonSRX
from wpilib import DigitalInput
from wpilib.command import Subsystem

import subsystems
from fusion.sensors import Manager, Report, ReportError, SensorService

# class IRService(SensorService):
#     POLL_RATE = 0.002  # s

#     ENTRY_BEND_BEAM_ID = "D1"
#     BOTTOM_BEND_BEAM_ID = "D2"
#     TOP_BEAM_ID = "D3"
#     EXIT_BEAM_ID = "D4"

#     def __init__(self):
#         super().__init__("IRService", IRService.POLL_RATE)

#         self._exit_beam = DigitalInput(IRService.EXIT_BEAM_ID)
#         self._top_beam = DigitalInput(IRService.TOP_BEAM_ID)
#         self._bottom_beam = DigitalInput(IRService.BOTTOM_BEAM_ID)
#         self._entry_beam = DigitalInput(IRService.ENTRY_BEND_BEAM_ID)

#         self.previous_state = (None, None, None, None)
#         self.current_state = (None, None, None, None)

#     class BreakReport(Report):
#         def __init__(self, service: SensorService):
#             super().__init__()

#             if service.previous_state == service.current_state:
#                 raise ReportError("IRService", "No Changes")

#             self.previous_state = service.previous_state
#             self.current_state = service.current_state

#     def update(self):
#         self.state_previous = self.state_current
#         self.state_current = (
#             self._exit_beam.get(),
#             self._top_beam.get(),
#             self._bottom_beam.get(),
#             self._entry_beam.get(),
#         )


class Indexer(Subsystem):
    """Controlled ball manager.

    Uses IR Light Breakage sensors to estimate ball position.
    """

    _instance = None

    TALON_ID = 40
    TALON_FPID = (0.0, 1.0, 0.0, 0.0)
    TALON_MAX_VELOCITY = 5  # m/s
    TALON_MAX_ACCELERATION = 2000  # ticks/100ms/s

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Indexer, cls).__init__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self._belt_controller = ctre.WPI_TalonFX(Indexer.TALON_ID)

        self._balls: List[Ball] = []

        self._belt_controller.config_kP(0, Indexer.TALON_FPID[1])
        self._belt_controller.config_kI(0, Indexer.TALON_FPID[2])
        self._belt_controller.config_kD(0, Indexer.TALON_FPID[3])

        self._belt_controller.configMotionAcceleration(Indexer.TALON_MAX_ACCELERATION)
        self._belt_controller.configMotionCruiseVelocity(Indexer.TARGET_VELOCITY)
        self._belt_controller.configMotionSCurveStrength(
            1
        )  # Smoothness from 1 to 8 (integer) (1 is a trapezoid)

        self._belt_controller.setSelectedSensorPosition(0)  # Zero the magnetic encoder

    def set_belt(self, control_mode: ControlMode, value):
        """Set the belt controller.

        Args:
            control_mode (ControlMode): Target ControlMode.
            value: Corresponding value.
        """
        self._belt_controller.set(control_mode, value)

    def turn_off(self):
        self._belt_controller.motorOff()

