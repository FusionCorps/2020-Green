from commandbased import CommandBasedRobot
from wpilib import run


class Green(CommandBasedRobot):
    def robotInit(self):
        import inputs
        from subsystems import i_chassis


if __name__ == "__main__":
    run(Green)
