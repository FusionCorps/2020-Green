from wpilib.command import Subsystem
from wpilib import DigitalInput
from ctre import WPI_TalonSRX, ControlMode
from fusion.sensors import SensorService, Manager, Report, ReportError

class UltrasoundService()
    
    SENSOR_L_ID = 'C3'
    SENSOR_R_ID = 'C4'
    
    def __init__(self):
        super().__init__("UltrasoundService")

        self._l_sensor = DigitalInput(UltrasoundService.SENSOR_L_ID)
        self._r_sensor = DigitalInput(UltrasoundService.SENSOR_R_ID)

        self.previous_state = (None, None)
        self.current_state = (None, None)

    class UltrasoundReport(Report):
        def __init__(self, service: SensorService):
            super().__init__()

            if service.previous_state == service.current_state:
                raise ReportError("IRService", "No Changes")

            self.previous_state = service.previous_state
            self.current_state = service.current_state
    
    def update(self):
        self.state_previous = self.state_current
        self.state_current = (self._l_sensor.get(), self._r_sensor.get())

    



class Climb(Subsystem):

    def __init__(self):
        pass
    
    @staticmethod
    def climb_calculator(m_6672, m_1, m_2, delta_x):
        report = Manager().get(UltrasoundService.UltrasoundReport)
        # TODO - Finish this - AO