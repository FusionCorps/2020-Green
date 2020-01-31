from wpilib.command import Subsystem
from enum import Enum
from ctre import WPI_TalonFX, ControlMode
from wpilib import DigitalInput
from typing import Optional
from fusion.sensors import SensorService, Report, ReportError, Manager

class IRService(SensorService):
    POLL_RATE = 0.002  # ms
    
    previous_state = True
    
    HORIZ_BEND_BEAM_ID = 'D1'
    VERT_BEND_BEAM_ID = 'D2'
    TOP_BEAM_ID = 'D3'


    class BreakReport(Report):
        def __init__(self, service):
            if service.state != service.previous_state:
                pass
            else:
                raise ReportError('IRService', 'No change.')

            self.beam_values = (service.bottom_beam_state, service.mid_beam_state, service.top_beam_state)
    
    def __init__(self):
        self._top_beam = DigitalInput(IRService.TOP_BEAM_ID)
        self._mid_beam = DigitalInput(IRService.END_BEAM_ID)
        self._bottom_beam = DigitalInput(IRService.HORIZ_BEND_BEAM_ID)

        self.top_beam_state = None
        self.mid_beam_state = None
        self.bottom_beam_state = None

    def update(self):
        self.top_beam_state = self._top_beam.get() # TODO
        self.mid_beam_state = self._mid_beam.get()  # TODO What is this method actually called
        self.bottom_beam_state = self._bottom_beam.get()


class Indexer(Subsystem):
    _instance = None

    MAX_SPEED = 5 # m/s

    class IndexerSpace(Enum):
        FULL = (True, True, True)
        EMPTY = (False, False, False)
        HORIZONTAL = (False, True, False)
        VERTICAL = (True, False, False)
        BOTH = (True, True, False)
        ONE = (False, True, True)


    TALON_HORIZ_ID = 11
    TALON_VERT_ID = 12

    class BallState(Enum):
        ENTERING = 0
        BOTTOM_CORNER = 1
        IN_CORNER = 2
        VERTICAL_CORNER = 3
        UNBUFFERED = 4
        SHOOTING = 5

    class FakeBall():
        def __init__(self):
            self.state = Indexer.BallState.ENTERING

        def change_state(self, new_state):
            self.state = new_state

        def return_state(self):
            return self.state
        

        



    '''
    Defines the motor IDs, beam IDs, and the State Enums for use later
    '''

    def __init__(self):
        self.vert_ball_count = 0

        self.horiz_belt_controller = WPI_TalonFX(Indexer.TALON_HORIZ_ID)
        self.vert_belt_controller = WPI_TalonFX(Indexer.TALON_VERT_ID)



        self.ball_list = []

        '''
        Define all the break beams and motor controllers
        Set the vertical ball count to 0
        '''
    @staticmethod
    def convert_ms_to_ticks(self, value: float) -> int:
        pass

    def get_state(self):
        report = Manager().get(IRService.BreakReport)

        for name, value in Indexer.IndexerSpace.__members__.items():
            if report.states == value:
                return value

    def add_ball(self):
        report = Manager().get(Camera.ThresholdReport)
    
    def update_balls(self):
        beam_report = Manager().get(IRService.BreakReport)
        '''Take beam report and cross check with predicted states'''
        if len(self.ball_list) == 1:
            if self.ball_list[0].state != Indexer.BallState.BOTTOM_CORNER and beam_report[0]:
                self.ball_list[0].state = Indexer.BallState.BOTTOM_CORNER
            elif self.ball_list[0].state != Indexer.BallState.VERTICAL_CORNER and beam_report[1]:
                self.ball_list[0].state = Indexer.BallState.VERTICAL_CORNER
            elif self.ball_list[0].state != Indexer.BallState.SHOOTING and beam_report[2]:
                self.ball_list[0].state = Indexer.BallState.SHOOTING
            '''This is going to be a lot of ugly casework if we don't streamline.
            If you see this, please try to make this wprk better than finding every case.'''
            



    def set_horiz_belt(self, active:bool, velocity: Optional[int] = None)      :
        if active:
            self.horiz_belt_controller.set(ControlMode.Velocity, velocity if velocity is not None else Indexer.MAX_SPEED)
        else:
            self.horiz_belt_controller.set(ControlMode.Velocity, 0)
    
    def set_vert_belt(self, active:bool, velocity: Optional[int] = None):
        if active:
            self.horiz_belt_controller.set(ControlMode.Velocity, velocity if velocity is not None else Indexer.MAX_SPEED)
        else:
            self.horiz_belt_controller.set(ControlMode.Velocity, 0)

       


    









