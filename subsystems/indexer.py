from wpilib.command import Subsystem
from enum import Enum
from ctre import WPI_TalonSRX, TalonSRXControlMode
from wpilib import DigitalInput
from typing import Optional
from fusion.sensors import SensorService, Report, ReportError, Manager
import ctre

class IRService(SensorService):
    POLL_RATE = 0.002  # ms
    
    previous_state = True
    
    HORIZ_BEND_BEAM_ID = 'D1'
    VERT_BEND_BEAM_ID = 'D2'
    TOP_BEAM_ID = 'D3'
    EXIT_BEAM_ID = 'D4'


    class BreakReport(Report):
        def __init__(self, service):
            if service.state != service.previous_state:
                pass
            else:
                raise ReportError('IRService', 'No change.')

            self.beam_values = (service.bottom_beam_state, service.mid_beam_state, service.top_beam_state, service.exit_beam_state)
    
    def __init__(self):
        self._exit_beam = DigitalInput(IRService.EXIT_BEAM_ID) 
        self._top_beam = DigitalInput(IRService.TOP_BEAM_ID)
        self._mid_beam = DigitalInput(IRService.END_BEAM_ID)
        self._bottom_beam = DigitalInput(IRService.HORIZ_BEND_BEAM_ID)

        self.exit_beam_state = None
        self.top_beam_state = None
        self.mid_beam_state = None
        self.bottom_beam_state = None

    def update(self):
        self.exit_beam_state = self._exit_beam.get()
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


    TALON_ID = 11
    
    TARGET_VELOCITY = 10000
    MAX_MOTOR_ACCELERATION = 2000 # ticks/100ms/s
 

    class BallState(Enum):
        ENTERING = 0
        BOTTOM_CORNER = 1
        IN_CORNER = 2
        VERTICAL_CORNER = 3
        UNBUFFERED = 4
        TOP = 5
        SHOOTING = 6

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
    

        self.belt_controller = WPI_TalonFX(Indexer.TALON_ID)




        self.ball_list = []

        self.belt_controller.config_kP(Shooter.PID_P_BELT)
        self.belt_controller.config_kI(Shooter.PID_I_BELT)
        self.belt_controller.config_kD(Shooter.PID_D_TALON_BELT)
        self.belt_controller.configMotionAcceleration(Shooter.MAX_MOTOR_ACCEL)
        self.belt_controller.configMotionCruiseVelocity(Shooter.TARGET_VELOCITY)
        self.belt_controller.configMotionSCurveStrength(1) # Smoothness from 1 to 8 (integer) (1 is a trapezoid)


        self.belt_controller.setSelectedSensorPosition(0)  # Zero the magnetic encoder

        '''
        Define all the break beams and motor controllers
        Set the vertical ball count to 0
        '''
    @staticmethod
    def convert_ms_to_ticks(self, value: float) -> int:
        pass

    def checkTop(self):
        report = Manager().get(IRService.BreakReport)
        return report[2]

    def setBeltTicks(self, ticks:int = 0):
        # Velocity is in encoder ticks per 100 ms
        self.belt_controller.set(TalonSRXControlMode.MotionMagic, ticks)






    
    


    

            

