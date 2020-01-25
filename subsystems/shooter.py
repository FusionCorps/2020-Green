from ctre import WPI_TalonSRX #NOTE: Change to WPI_TalonFX when libraries update
from wpilib.command import Subsystem
from wpilib import IterativeRobot
from wpilib import PIDController

#NOTE: investigate using the motion magic on the motor

class Robot(IterativeRobot):
    def __init__(self):
        super.__init__("Robot")

        self.motorContollerTop = WPI_TalonSRX(5)
        self.PIDControllerTop = PIDController(1.0, 0.0, 0.0)

    def teleopInit(self):
        self.motorContollerTop.set(self.PIDControllerTop.get(self.motorContollerTop.getSensorCollection().getIntegatedSensorVelocity()))
