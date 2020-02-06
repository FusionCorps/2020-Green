from time import sleep
from wpilib.command import Subsystem
from enum import Enum
from ctre import WPI_TalonFX, ControlMode
from wpilib import DigitalInput
from typing import Optional
from fusion.sensors import SensorService, Report, ReportError, Manager

class IRService(SensorService):
    POLL_RATE = 0.002  # s
    
    HORIZ_BEND_BEAM_ID = 'D1'
    VERT_BEND_BEAM_ID = 'D2'
    TOP_BEAM_ID = 'D3'
    BOTTOM_BEAM_ID = 'D4'

    class BreakReport(Report):
        def __init__(self, service: SensorService):
            super().__init__()

            if service.previous_state == service.state:
                raise ReportError("IRService", "No Changes")

            self.previous_state = service.previous_state
            self.state = service.state
    

    def __init__(self):
        super().__init__("IRService", IRService.POLL_RATE)
        
        self._entry_sensor = DigitalInput(IRService.HORIZ_BEND_BEAM_ID)
        self._bottom_sensor = DigitalInput(IRService.BOTTOM_BEAM_ID) 
        self._top_sensor = DigitalInput(IRService.TOP_BEAM_ID)
        self._exit_sensor = DigitalInput(IRService.VERT_BEND_BEAM_ID)

        self.previous_state = (None, None, None, None)
        self.current_state = (None, None, None, None)

    def update(self):
        self.previous_state = self.current_state
        self.current_state = (self._entry_sensor.get(), self._bottom_sensor.get(), self._top_sensor.get(), self._exit_sensor.get())
