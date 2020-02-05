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
    

