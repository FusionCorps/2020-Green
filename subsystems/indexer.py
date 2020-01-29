from wpilib.command import Subsystem
from enum import Enum
from ctre import WPI_TalonFX, ControlMode
import digitalio
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

        self.top_beam = digitalio.DigitalInOut(Indexer.TOP_BEAM_ID)
        self.top_beam.direction = digitalio.Direction.INPUT
        self.top_beam.pull = digitalio.Pull.UP

        self.mid_beam = digitalio.DigitalInOut(Indexer.VERT_BEND_BEAM_ID)
        self.mid_beam.direction = digitalio.Direction.INPUT
        self.mid_beam.pull = digitalio.Pull.UP

        self.bottom_beam = digitalio.DigitalInOut(Indexer.HORIZ_BEND_BEAM_ID)
        self.bottom_beam.direction = digitalio.Direction.INPUT
        self.bottom_beam.pull = digitalio.Pull.UP

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
        if self.mid_beam.value:
            self.vert_state = Indexer.VerticalIndexerState.SPACE_AVAILABLE
        else:
            self.vert_state = Indexer.VerticalIndexerState.NO_SPACE
        
        return self.vert_state
    
    def get_horiz_state(self):
        '''Check sensors and return state: Horizontal'''

        if self.bottom_beam.value:
            self.horiz_state = Indexer.HorizontalIndexerState.BALL_NOT_READY
        else:
            self.horiz_state = Indexer.HorizontalIndexerState.BALL_READY
        return self.horiz_state

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

    def load_to_top(self, active:bool):
        self.loading = True
        while self.loading:
            if self.horiz_state is Intake.HorizontalIndexerState.BALL_READY and self.VerticalIndexerState is Intake.VerticalIndexerState.SPACE_AVAILABLE:
                set_horiz_belt(True)
                set_vert_belt(True)
            if self.horiz_state is Intake.HorizontalIndexerState.BALL_READY and self.VerticalIndexerState is not Intake.VerticalIndexerState.SPACE_AVAILABLE:
                set_horiz_belt(False)
                set_vert_belt(True)
            if self.horiz_state is not Intake.HorizontalIndexerState.BALL_READY and self.VerticalIndexerState is Intake.VerticalIndexerState.SPACE_AVAILABLE:
                set_horiz_belt(True)
                set_vert_belt(False)
            if self.horiz_state is not Intake.HorizontalIndexerState.BALL_READY and self.VerticalIndexerState is not Intake.VerticalIndexerState.SPACE_AVAILABLE:
                set_horiz_belt(True)
                set_vert_belt(True)
            
    def stop_loading(self):
        self.loading = False

    









