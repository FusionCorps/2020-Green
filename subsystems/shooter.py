import enum
import logging

import ctre
import wpilib
from wpilib.command import Subsystem

from math import *


class Shooter(Subsystem):
    _instance = None

    ANGLE = pi / 2

    ID_TALON_LEFT = 0
    ID_TALON_RIGHT = 1

    TALON_LEFT_FPID = (0.0, 1.0, 0.0, 0.0)
    TALON_RIGHT_FPID = (0.0, 1.0, 0.0, 0.0)
    TALON_TURRET_FPID = (0.0, 1.0, 0.0, 0.0)

    ID_TALON_TURRET = 14





    MAX_VELOCITY = 20480  # encoder ticks/100ms

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

        self._talon_l.setInverted(True)  # Left motor mounted opposite right one
        self._talon_l.configSelectedFeedbackSensor(
            ctre.FeedbackDevice.CTRE_MagEncoder_Relative
        )  # Magnetic encoder should be relative to starting measurement point
        self._talon_l.setSensorPhase(
            True
        )  # Encoder feedback should read positive even if left motor is flipped

        self._talon_r.follow(self._talon_l)  # Makes left motor the master controller

        # TODO Check what Peak Nominal and Output configs do and add them

        self.target_velocity = 20000 # Ticks/100ms

        """PIDF Constants"""
        self._talon_l.config_kP(Shooter.TALON_LEFT_FPID[1])
        self._talon_l.config_kI(Shooter.TALON_LEFT_FPID[2])
        self._talon_l.config_kD(Shooter.TALON_LEFT_FPID[3])

        self._talon_l.configCruiseVelocity(20000)
        self._talon_l.configAcceleration(10000)
        self._talon_l.configSCurveStrength(1)

        self._talon_l.setSelectedSensorPosition(0)  # Zero the magnetic encoder

        self._talon_turret = WPI_TalonFX(Shooter.ID_TALON_TURRET)

        self._talon_turret.config_kP(Shooter.TALON_TURRET_FPID[1])
        self._talon_turret.config_kI(Shooter.TALON_TURRET_FPID[2])
        self._talon_turret.config_kD(Shooter.TALON_TURRET_FPID[3])        

        self._talon_turret.configCruiseVelocity(20000)
        self._talon_turret.configAcceleration(10000)
        self._talon_turret.configSCurveStrength(1)

        self._talon_turret.setSelectedSensorPosition(ctre.FeedbackDevice.CTRE_MagEncoder_Relative)



    def get_state(self):
        return self._state

    @staticmethod
    def calculate_angular_velocity(
        distance: float, height: float, shooter_angle: float = Shooter.ANGLE
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

    def set_state(self, state: Shooter.State):
        self._state = state

    def set(self, control_mode: ControlMode, value):
        self._talon_l.set(mode=control_mode, demand0=value)

    def get(self):
        self._talon_l.getSelectedSensorPosition()
    
    def set_turret(self, control_mode: ControlMode, value):
        self._talon_turret.set(mode=control_mode, demand0=value)
    
    shooter = Shooter()

