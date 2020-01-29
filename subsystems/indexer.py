from wpilib.command import Subsystem
from enum import Enum
from ctre import WPI_TalonFX, ControlMode
from wpilib import DigitalInput
from typing import Optional

class Indexer(Subsystem):
    _instance = None
    MAX_SPEED = 5 #m/s
    class VerticalIndexerState(Enum):
        SPACE_AVAILABLE = 0
        NO_SPACE = 1
    
    class HorizontalIndexerState(Enum):
        BALL_READY = 0
        BALL_NOT_READY = 1
    
    TALON_HORIZ_ID = 11
    TALON_VERT_ID = 12

    HORIZ_BEND_BEAM_ID = 'D1'
    VERT_BEND_BEAM_ID = 'D2'
    TOP_BEAM_ID = 'D3'

    '''
    Defines the motor IDs, beam IDs, and the State Enums for use later
    '''

    def __init__(self):
        self.vert_ball_count = 0

        self.horiz_belt_controller = WPI_TalonFX(Indexer.TALON_HORIZ_ID)
        self.vert_belt_controller = WPI_TalonFX(Indexer.TALON_VERT_ID)

        self.top_beam = DigitalInput(Indexer.TOP_BEAM_ID)

        self.mid_beam = DigitalInput(Indexer.VERT_BEND_BEAM_ID)

        self.bottom_beam = DigitalInput(Indexer.HORIZ_BEND_BEAM_ID)

        self.is_on = True

        '''
        Define all the break beams and motor controllers
        Set the vertical ball count to 0
        '''
    @staticmethod
    def convert_ms_to_ticks(self, value: float) -> int:
        pass
    
    def get_vert_state(self):
        '''Check sensors and return state: Vertical'''
        if self.top_beam.value:
            self.vert_state = Indexer.VerticalIndexerState.SPACE_AVAILABLE
        else:
            self.vert_state = Indexer.VerticalIndexerState.NO_SPACE
        
        return self.vert_state

    
    def set_vert_state(self):
        '''Check sensors and return state: Vertical'''
        if self.top_beam.value:
            self.vert_state = Indexer.VerticalIndexerState.SPACE_AVAILABLE
        else:
            self.vert_state = Indexer.VerticalIndexerState.NO_SPACE

    def get_horiz_state(self):
        '''Check sensors and return state: Horizontal'''

        if self.bottom_beam.value:
            self.horiz_state = Indexer.HorizontalIndexerState.BALL_NOT_READY
        else:
            self.horiz_state = Indexer.HorizontalIndexerState.BALL_READY
        return self.horiz_state

    def set_horiz_state(self):
        '''Check sensors and set state: Horizontal'''

        if self.bottom_beam.value:
            self.horiz_state = Indexer.HorizontalIndexerState.BALL_NOT_READY
        else:
            self.horiz_state = Indexer.HorizontalIndexerState.BALL_READY
        

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

    def corner_pass(self, active:bool):
        '''To be called when a ball is available and space is avalilable.
        After there will be may or may not be space and there may or may not be a ball available'''
        if active:
            self.set_horiz_state()
            self.set_vert_state()
            if self.horiz_state == Indexer.HorizontalIndexerState.BALL_READY and self.vert_state == Indexer.VerticalIndexerState.SPACE_AVAILABLE:
                while not self.bottom_beam.value:
                    self.set_horiz_belt(True)
                    self.set_vert_belt(True)
                self.set_horiz_belt(False)
                self.set_vert_belt(False)
                self.set_horiz_state()
                self.set_vert_state()
        
    def load_to_top(self, active:bool):
        '''Load balls in vertical chute to top regardless of horizontal state
        Vertical state should start with available space and end without available space'''
        if active:
            self.set_horiz_state()
            self.set_vert_state()
            if self.vert_state == Indexer.VerticalIndexerState.SPACE_AVAILABLE:
                while self.top_beam.value:
                    self.set_vert_belt(True)
                self.set_vert_belt(False)
                self.set_horiz_state()
                self.set_vert_state()
    
    def load_to_corner(self, active:bool):
        '''Load balls in horizontal tube to the corner
        Horizontal state should start in ball not available'''
        if active:
            self.set_horiz_state()
            if self.horiz_state == Indexer.HorizontalIndexerState.BALL_NOT_READY:
                while self.bottom_beam.value:
                    self.set_horiz_belt(True)
                self.set_horiz_belt(False)
                self.set_horiz_state()
                self.set_vert_state()

    



        



            
    def stop_loading(self):
        self.loading = False

    









