from commandbased import CommandBasedRobot
from wpilib import run
from subsystems import chassis
import inputs

class Green(CommandBasedRobot):
    def robotInit(self):
        pass


if __name__ == "__main__":
    run(Green)
