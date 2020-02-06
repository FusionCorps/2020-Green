from wpilib.command import Command
from subsystems.indexer import Indexer

class CornerPass(Command):
    def initialize(self):
        pass

    def execute(self):
        Indexer().set_horiz_belt(True)
        Indexer().set_vert_belt(True)
        Indexer().set_horiz_state()
        Indexer().set_vert_state()


    def isFinished(self):
        return bool Indexer().horiz_state == Indexer().HorizontalIndexerState.BALL_NOT_READY
        #TO DO: fix this cuz it aint right  

    def end(self):
        pass

    def interrupted(self):
        pass



