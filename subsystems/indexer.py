from enum import Enum
from time import sleep
from typing import Optional

import ctre
from ctre import ControlMode, WPI_TalonSRX
from wpilib import DigitalInput
from wpilib.command import Subsystem

import subsystems
from fusion.sensors import Manager, Report, ReportError, SensorService\
from fusion.ball_class import VirtualBall

class IRService(SensorService):
    POLL_RATE = 0.002  # s

    ENTRY_BEND_BEAM_ID = "D1"
    BOTTOM_BEND_BEAM_ID = "D2"
    TOP_BEAM_ID = "D3"
    EXIT_BEAM_ID = "D4"

    def __init__(self):
        super().__init__("IRService", IRService.POLL_RATE)

        self._exit_beam = DigitalInput(IRService.EXIT_BEAM_ID)
        self._top_beam = DigitalInput(IRService.TOP_BEAM_ID)
        self._bottom_beam = DigitalInput(IRService.BOTTOM_BEAM_ID)
        self._entry_beam = DigitalInput(IRService.ENTRY_BEND_BEAM_ID)

        self.previous_state = (None, None, None, None)
        self.current_state = (None, None, None, None)

    class BreakReport(Report):
        def __init__(self, service: SensorService):
            super().__init__()

            if service.previous_state == service.current_state:
                raise ReportError("IRService", "No Changes")

            self.previous_state = service.previous_state
            self.current_state = service.current_state

    def update(self):
        self.state_previous = self.state_current
        self.state_current = (
            self._exit_beam.get(),
            self._top_beam.get(),
            self._bottom_beam.get(),
            self._entry_beam.get(),
        )


class Indexer(Subsystem):
    _instance = None

    MAX_SPEED = 5  # m/s
    TALON_ID = 11

    TALON_ID = 11

    TARGET_VELOCITY = 10000  # ticks/100ms
    MAX_MOTOR_ACCELERATION = 2000  # ticks/100ms/s

        def change_state(self, new_state):
            self.state = new_state

        def return_state(self):
            return self.state

    class IndexerState(Enum):
        RUNNING = 0  # Belts moving
        NOT_READY = 1  # No ball at top
        READY = 2  # Ball at top

    """
    Defines the motor IDs, beam IDs, and the State Enums for use later
    The ball states and fake ball might or might not be outdated
    """

    def __init__(self):

        self.belt_controller = WPI_TalonFX(Indexer.TALON_ID)

        self.belt_controller.config_kP(Indexer.PID_P_BELT)
        self.belt_controller.config_kI(Indexer.PID_I_BELT)
        self.belt_controller.config_kD(Indexer.PID_D_TALON_BELT)
        self.belt_controller.configMotionAcceleration(Indexer.MAX_MOTOR_ACCEL)
        self.belt_controller.configMotionCruiseVelocity(Indexer.TARGET_VELOCITY)
        self.belt_controller.configMotionSCurveStrength(
            1
        )  # Smoothness from 1 to 8 (integer) (1 is a trapezoid)

        self.belt_controller.setSelectedSensorPosition(0)  # Zero the magnetic encoder

        self.ball_list = []

        """
        Define all the break beams and motor controllers
        Create the ball list
        """


    @staticmethod
    def convert_ms_to_ticks(self, value: float) -> int:
        pass

    # def checkTop(self):
    #     report = Manager().get(IRService.BreakReport)
    #     return report[2]

    def set_belt_ticks(self, ticks: int = 0):
        # Angle in encoder ticks
        self.belt_controller.set(ControlMode.MotionMagic, ticks)

    def set_belt_velocity(self, velocity):
        self.belt_controller.set(ControlMode.Velocity, velocity)

    def set_belt_percentage(self, percentage):
        self.belt_controller.set(ControlMode.Percentage, percentage)

    def turn_off(self):
        self.belt_controller.motorOff()

    def add_ball(self):
        new_ball = Indexer.FakeBall(self.belt_controller.getSelectedSensorPosition())
        ball_list.insert(new_ball)

    def remove_ball(self, pos = -1):
        ball_list.pop(pos)

    def get_ball_pos(self):
        positions = []
        for ball in ball_list:
            position.append(self.belt_controller.getSelectedSensorPosition() - ball.init_pos)
        return positions

    def check_top(self):
        report = Manager().get(IRService.BreakReport)
        return report[2]

     