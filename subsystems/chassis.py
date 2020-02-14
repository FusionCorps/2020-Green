"""
Chassis functionality.
"""
from ctre import WPI_TalonSRX
from wpilib.command import Subsystem
from wpilib.drive import DifferentialDrive

from fusion.unique import unique


@unique
class Chassis(Subsystem):
    """
    Singleton subsystem containing all driving functionality.
    """

    # Controller IDs listed counter-clockwise
    TALON_F_R_ID = 1
    TALON_F_L_ID = 0
    TALON_B_L_ID = 2
    TALON_B_R_ID = 3

    def __init__(self):
        super().__init__("Chassis")

        # Speed Controllers
        self._talon_f_r = WPI_TalonSRX(Chassis.TALON_F_R_ID)
        self._talon_f_l = WPI_TalonSRX(Chassis.TALON_F_L_ID)
        self._talon_b_l = WPI_TalonSRX(Chassis.TALON_B_L_ID)
        self._talon_b_r = WPI_TalonSRX(Chassis.TALON_B_R_ID)

        self._talon_b_l.follow(self._talon_f_l)
        self._talon_b_r.follow(self._talon_f_r)

        self._drive = DifferentialDrive(self._talon_f_l, self._talon_f_r)

    def joystick_drive(self, x_axis: int, y_axis: int) -> None:
        """Drive the Chassis using joystick input.

        Sets the DifferentialDrive object's speed using the
        provided joystick inputs.

        Args:
            x_axis (int): Value for the magnitude of the movement
            y_axis (int): Value for the rotation of the movement
        """
        self._drive.curvatureDrive(x_axis, y_axis, True)

    def initDefaultCommand(self):
        from commands.chassis import JoystickDrive

        self.setDefaultCommand(JoystickDrive)
