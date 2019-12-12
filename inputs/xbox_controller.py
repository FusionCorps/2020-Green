from wpilib import Joystick
from wpilib.buttons import JoystickButton

import robotmap


class XBoxController(Joystick):
    def __init__(self, port: int = robotmap.joystick):
        super().__init__(port)

        buttons = {
            'a': 1,
            'b': 2,
            'x': 3,
            'y': 4,
            'bumper_l': 5,
            'bumper_r': 6,
            'back': 7,
            'start': 8,
            'l_3': 9,
            'r_3': 10
            }

        for button, number in buttons.items():
            self.__dict__[str(button)] = JoystickButton(self, number)

    def get_x(self):
        return self.getRawAxis(1)

    def get_y(self):
        return -self.getRawAxis(4)

    def get_l_trigger(self):
        return self.getRawAxis(2)

    def get_r_trigger(self):
        return self.getRawAxis(3)