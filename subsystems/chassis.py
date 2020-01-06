from rev import CANSparkMax, MotorType
from wpilib.command import Subsystem
from wpilib.drive import DifferentialDrive


class Chassis(Subsystem):
    def __init__(self):
        super().__init__("Chassis")

        self.l_controller = CANSparkMax(0, MotorType.kBrushless)
        self.r_controller = CANSparkMax(1, MotorType.kBrushless)

        self.drive = DifferentialDrive(self.l_controller, self.r_controller)

    def joystick_drive(self, x_axis: float, y_axis: float) -> None:
        self.drive.curvatureDrive(x_axis, y_axis, True)

    def initDefaultCommand(self):
        from commands.joystick_drive import JoystickDrive

        self.setDefaultCommand(JoystickDrive())
