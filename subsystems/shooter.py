from ctre import WPI_TalonFX
from wpilib.command import Subsystem
from wpilib import TimedRobot
from wpilib import PIDController

class Robot(TimedRobot):
    def __init__(self):
        super.__init__("Robot")

        self.motorContollerTop = WPI_TalonFX(5)
        self.PIDControllerTop = PIDController(1.0, 0.0, 0.0)

    def teleopInit(self):
        self.motorContollerTop.set(self.PIDControllerTop.calculate(self.motorContollerTop.getSensorCollection().getIntegatedSensorVelocity()))
