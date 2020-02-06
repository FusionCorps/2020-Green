from time import sleep
from wpilib.command import Subsystem
from enum import Enum
from ctre import WPI_TalonSRX, TalonSRXControlMode
from wpilib import DigitalInput
from typing import Optional
from fusion.sensors import SensorService, Report, ReportError, Manager
import ctre


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
            self._entry_beam.get()
        )


class Indexer(Subsystem):
    _instance = None

    MAX_SPEED = 5  # m/s
    TALON_ID = 11




    TALON_ID = 11
    
    TARGET_VELOCITY = 10000 # ticks/100ms
    MAX_MOTOR_ACCELERATION = 2000 # ticks/100ms/s
 

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
    The ball states and fake ball might or might not be outdated
    """

    def __init__(self):
    

        self.belt_controller = WPI_TalonFX(Indexer.TALON_ID)

        self.ball_list = []

        self.belt_controller.config_kP(Shooter.PID_P_BELT)
        self.belt_controller.config_kI(Shooter.PID_I_BELT)
        self.belt_controller.config_kD(Shooter.PID_D_TALON_BELT)
        self.belt_controller.configMotionAcceleration(Shooter.MAX_MOTOR_ACCEL)
        self.belt_controller.configMotionCruiseVelocity(Shooter.TARGET_VELOCITY)
        self.belt_controller.configMotionSCurveStrength(1) # Smoothness from 1 to 8 (integer) (1 is a trapezoid)

        self.belt_controller.setSelectedSensorPosition(0)  # Zero the magnetic encoder

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

    def setBeltTicks(self, ticks:int = 0):
        # Angle in encoder ticks
        self.belt_controller.set(TalonSRXControlMode.MotionMagic, ticks)


