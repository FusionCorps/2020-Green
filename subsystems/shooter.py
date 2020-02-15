from enum import Enum
from math import cos, pi, sin, sqrt

import ctre
from wpilib.command import Subsystem

from fusion.unique import unique


@unique
class Shooter(Subsystem):
    ANGLE = pi / 2

    ID_TALON_LEFT = 0
    ID_TALON_RIGHT = 1

    PID_P_TALON_LEFT = 1.0
    PID_I_TALON_LEFT = 0.0
    PID_D_TALON_LEFT = 0.0
    PID_F_TALON_LEFT = 0.0

    MAX_VELOCITY = 20480  # encoder ticks/100ms

    class ShooterState(Enum):
        STOPPED = 0  # Wheel stopped
        SPOOLING = 1  # Wheel speeding up
        WAITING = 2  # Wheel at speed; waiting for ball
        SHOOTING = 3  # Wheel at speed; ball loading
        SLOWING = 4  # Wheel slowing down

    def __init__(self):
        super().__init__("Shooter")

        self._state = Shooter.ShooterState.STOPPED

        self._talon_l = ctre.WPI_TalonFX(Shooter.ID_TALON_LEFT)
        self._talon_r = ctre.WPI_TalonFX(Shooter.ID_TALON_RIGHT)

        self._talon_l.setInverted(True)  # Left motor mounted opposite right one
        self._talon_l.configSelectedFeedbackSensor(
            ctre.FeedbackDevice.CTRE_MagEncoder_Relative
        )  # Magnetic encoder should be relative to starting measurement point
        self._talon_l.setSensorPhase(
            True
        )  # Encoder feedback should read positive even if left motor is flipped

        self._talon_r.follow(self._talon_l)  # Makes left motor the master controller

        # FPID Constants
        self._talon_l.config_kP(0, Shooter.PID_P_TALON_LEFT)
        self._talon_l.config_kI(0, Shooter.PID_I_TALON_LEFT)
        self._talon_l.config_kD(0, Shooter.PID_D_TALON_LEFT)

        self._talon_l.setSelectedSensorPosition(0)  # Zero the magnetic encoder

    def get_state(self):
        return self._state

    def get_velocity(self):
        return self._talon_l.getSelectedSensorVelocity()

    @staticmethod
    def calculate_angular_velocity(
        distance: float, height: float, shooter_angle: float
    ):
        # Angle needs to be in RADIANS
        v_rob = 0
        height = 2.49  # meters

        velocity = (
            2 * v_rob * cos(shooter_angle)
            - v_rob * sin(shooter_angle) * distance
            + sqrt(
                (2 * v_rob * cos(shooter_angle) - v_rob * sin(shooter_angle) * distance)
                ** 2
                + 4
                * (
                    sin(shooter_angle) * cos(shooter_angle) * distance
                    - height * cos(shooter_angle) ** 2
                )
                * (9.8 * distance ** 2 / 2 + v_rob ** 2)
            )
        ) / (
            2
            * (
                sin(shooter_angle) * cos(shooter_angle) * distance
                - height * cos(shooter_angle) ** 2
            )
        )

        omega = 2 * velocity / 0.1016  # radians/second
        converted_omega = 102.4 / pi * omega  # encoder ticks/100ms

        return converted_omega

    def set_state(self, state):
        self._state = state

    def set(self, control_mode: ctre.ControlMode, value):
        self._talon_l.set(mode=control_mode, demand0=value)
