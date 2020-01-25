import enum
import logging

import commandbased as cmd
import ctre
import wpilib
from wpilib.command import Subsystem


class Shooter(Subsystem):
    _instance = None

    ID_TALON_LEFT = 0
    ID_TALON_RIGHT = 1

    PID_P_TALON_LEFT = 1.0
    PID_I_TALON_LEFT = 0.0
    PID_D_TALON_LEFT = 0.0
    PID_F_TALON_LEFT = 0.0

    class State(enum.Enum):
        STOPPED = 0  # Wheel stopped
        SPOOLING = 1  # Wheel speeding up
        WAITING = 2  # Wheel at speed; waiting for ball
        SHOOTING = 3  # Wheel at speed; ball loading
        SLOWING = 4  # Wheel slowing down

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Shooter, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        super.__init__("Shooter")

        self._state = Shooter.State.STOPPED

        self._talon_l = ctre.WPI_TalonFX(Shooter.ID_TALON_LEFT)
        self._talon_r = ctre.WPI_TalonFX(Shooter.ID_TALON_RIGHT)

        self._talon_l.setInverted(True)  # Left motor mounted opposite Right
        self._talon_l.configSelectedFeedbackSensor(
            ctre.FeedbackDevice.CTRE_MagEncoder_Relative
        )
        self._talon_l.setSensorPhase(True)  # Encoder feedback should read positive

        self._talon_r.follow(self._talon_l)

        # TODO Check what Peak Nominal and Output configs do and add them

        self._talon_l.config_kP(Shooter.PID_P_TALON_LEFT)
        self._talon_l.config_kI(Shooter.PID_I_TALON_LEFT)
        self._talon_l.config_kD(Shooter.PID_D_TALON_LEFT)

        self._talon_l.setSelectedSensorPosition(0)

    def set_state(self, state: Shooter.State):
        if state == self._state:
            return

