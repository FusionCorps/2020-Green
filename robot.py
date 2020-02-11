from commandbased import CommandBasedRobot
from wpilib import run, SmartDashboard


class Green(CommandBasedRobot):
    def robotInit(self):
        import inputs
        import subsystems
        import commands

    def robotPeriodic(self):
        import subsystems

        SmartDashboard().putNumberArray("Indexer FPID", subsystems.Indexer().TALON_FPID)
        Indexer.TALON_FPID = SmartDashboard().getNumberArray(
            "Indexer FPID", [0.0, 0.1, 0.0, 0.0]
        )


if __name__ == "__main__":
    run(Green)
