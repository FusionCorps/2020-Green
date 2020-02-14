import ctre
from ctre import ControlMode
from wpilib.command import Subsystem

from fusion.unique import unique


@unique
class Indexer(Subsystem):
    """Controlled ball manager.

    Uses IR Light Breakage sensors to estimate ball position.
    """

    TALON_ID = 40
    TALON_FPID = (0.0, 0.1, 0.0, 0.0)
    TALON_MAX_VELOCITY = 5  # m/s
    TALON_MAX_ACCELERATION = 2000  # ticks/100ms/s

    BALL_MOVEMENT_TICKS = 2  # m

    def __init__(self):
        self._belt_controller = ctre.WPI_TalonFX(Indexer.TALON_ID)

        self._belt_controller.config_kP(0, Indexer.TALON_FPID[1])
        self._belt_controller.config_kI(0, Indexer.TALON_FPID[2])
        self._belt_controller.config_kD(0, Indexer.TALON_FPID[3])

        self._belt_controller.configMotionAcceleration(Indexer.TALON_MAX_ACCELERATION)
        self._belt_controller.configMotionCruiseVelocity(Indexer.TALON_MAX_VELOCITY)
        self._belt_controller.configMotionSCurveStrength(
            1
        )  # Smoothness from 1 to 8 (integer) (1 is a trapezoid)

        self._belt_controller.setSelectedSensorPosition(0)  # Zero the magnetic encoder

    def set_belt(self, control_mode: ControlMode, value) -> None:
        """Set the belt controller.

        Args:
            control_mode (ControlMode): Target ControlMode.
            value: Corresponding value.
        """
        self._belt_controller.set(control_mode, value)

    def turn_off(self) -> None:
        self._belt_controller.motorOff()

    def get_position(self) -> int:
        return self._belt_controller.getSelectedSensorPosition()

    def zero_encoder(self) -> None:
        self._belt_controller.setSelectedSensorPosition(0)
