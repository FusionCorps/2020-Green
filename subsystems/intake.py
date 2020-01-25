from ctre import WPI_TalonFX
from wpilib.command import Subsystem
from wpilib import TimedRobot
from wpilib import PIDController

class Robot(TimedRobot):
    def __init__(self):
        super.__init__("Robot")

        self.motorContollerBottom = WPI_TalonFX(6)
        self.PIDControllerBottom = PIDController(1.0, 0.0, 0.0)

    def teleopInit(self):
        self.motorContollerBottom.set(self.PIDControllerBottom.calculate(self.motorContollerBottom.getSensorCollection().getIntegatedSensorVelocity()))
