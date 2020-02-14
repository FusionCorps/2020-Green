from enum import Enum

class VirtualBall():

    class BallState(Enum):
        INTAKE = 0
        HOPPER = 1
        INDEXER = 2
        SHOOTER = 3

    def __init__(self, pos = None):
        self.state = VirtualBall.BallState.INTAKE 
        self.pos = pos # Indexer position
