import board
import digitalio
from wpilib.command import Subsystem
from ctre import WPI_TalonFX
 
# Create digital input with pull-up resistor on pin D5
# for break beam sensor.
break_beam = digitalio.DigitalInOut(board.D5)
break_beam.direction = digitalio.Direction.INPUT
break_beam.pull = digitalio.Pull.UP



class Intake(Subsystem):
    def __init(self):
        super.__init__('Intake')

        BREAK_BEAM_TOP_ID = 0
        BREAK_BEAM_VERT_CORNER_ID = 1
        BREAK_BEAM_HORIZ_CORNER_ID = 2
        BREAK_BEAM_ENTRY_ID = 3

        VERT_BELT_MOTOR_ID = 13
        HORIZ_BELT_MOTOR_ID = 14

        self.belt_velocity_vert = 409 #default is two rotations per second (120 RPM)
        self.belt_velocity_horiz = 409 #default is two rotations per second (120 RPM)

        self.is_loading = False

        self.ball_count_horiz = 0
        self.ball_count_vert = 0

        self.break_beam_entry = digitalio.DigitalInOut(board.BREAK_BEAM_ENTRY_ID)
        self.break_beam_entry.direction = digitalio.Direction.INPUT
        self.break_beam_entry.pull = digitalio.Pull.UP
        
        self.break_beam_horiz_corner = digitalio.DigitalInOut(board.BREAK_BEAM_HORIZ_CORNER_ID)
        self.break_beam_horiz_corner.direction = digitalio.Direction.INPUT
        self.break_beam_horiz_corner.pull = digitalio.Pull.UP
        
        self.break_beam_vert_corner = digitalio.DigitalInOut(board.BREAK_BEAM_VERT_CORNER_ID)
        self.break_beam_vert_corner.direction = digitalio.Direction.INPUT
        self.break_beam_vert_corner.pull = digitalio.Pull.UP
        
        self.break_beam_top = digitalio.DigitalInOut(board.BREAK_BEAM_TOP_ID)
        self.break_beam_top.direction = digitalio.Direction.INPUT
        self.break_beam_top.pull = digitalio.Pull.UP

        self.beltControllerVert = WPI_TalonFX(VERT_BELT_MOTOR_ID)
        self.beltControllerHoriz = WPI_TalonFX(HORIZ_BELT_MOTOR_ID)

        
    
    def load_to_top(self):
        while self.break_beam_top.value:
            self.beltControllerVert.set(self.belt_velocity_vert)
            break
    
    def load_to_corner(self):
        while self.break_beam_horiz_corner.value:
            self.beltControllerVert.set(self.belt_velocity_horiz)

'''
To finish - write corner handoff code to add 1 in. buffer between balls in 
vertical chute. 
''' 


        

        


