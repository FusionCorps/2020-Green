from ctre import VictorSPX, ControlMode
from wpilib.command import Subsystem
from _pynetworktables import NetworkTables
from fusion.networktable import robot_table

class Intake(Subsystem):

    VICTOR_ID = 9

    INTAKE_PIDF = (1.0, 0.0 , 0.0, 0.0)
    INTAKE_VEL_ACCEL_CURVE = (20000, 10000, 1)

    def __init__(self):
        self.intake_controller = VictorSPX(Intake.VICTOR_ID)

        self.intake_controller.config_kP(Intake.INTAKE_PIDF[0])
        self.intake_controller.config_kI(Intake.INTAKE_PIDF[1])
        self.intake_controller.config_kD(Intake.INTAKE_PIDF[2])
        self.intake_controller.config_kF(Intake.INTAKE_PIDF[3])
        
        self.intake_controller.configCruiseVelocity(Intake.INTAKE_VEL_ACCEL_CURVE[0])
        self.intake_controller.configAcceleration(Intake.INTAKE_VEL_ACCEL_CURVE[1])
        self.intake_controller.configSCurveStrength(Intake.INTAKE_VEL_ACCEL_CURVE[2])

        self.ball_list = []

        self.is_on = False

    def set_intake(self, velocity:float):
        # Velocity is in ticks/100ms
        self.intake_controller.set(ControlMode.Velocity, velocity)

    def turn_off(self):
        self.intake_controller.stopMotor()

    def push_state(self):
        robot_table.putBoolean('IntakeState', self.is_on)

intake = Intake()