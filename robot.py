from wpilib.command import Scheduler
from wpilib import SmartDashboard
from networktables import NetworkTables
import logging
from commandbased import CommandBasedRobot
from wpilib import run


class Green(CommandBasedRobot):
    def robotInit(self):
        import inputs
        import subsystems
        import commands

        self.logger = logging.getLogger("Green")

        NetworkTables.initialize(server="roborio-6672-frc.local")

        self.sd = NetworkTables.getTable("SmartDashboard")
        self.sd.putString(
            "ChassisCurrentCommand", subsystems.Chassis().getCurrentCommandName()
        )

    def teleopPeriodic(self):
        import subsystems
        from ctre import ControlMode

        # subsystems.Chasses()._talon_f_r.set(ControlMode.PercentOutput, 0.1)
        # self.logger.info(subsystems.Chassis()._talon_f_r.get())
        # self.logger.info(commands.chassis.ChassisJoystickDrive().isRunning())

        Scheduler.getInstance().run()


if __name__ == "__main__":
    run(Green)
