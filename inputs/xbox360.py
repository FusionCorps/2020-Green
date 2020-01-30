from functools import partial
from weakref import WeakKeyDictionary

from wpilib import Joystick
from wpilib.buttons import JoystickButton


class XBoxController(Joystick):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(XBoxController, cls).__new__(cls)
        return cls._instance

    def __init__(self, port: int):
        super().__init__(port)

        items = {
            "a": 1,
            "b": 2,
            "x": 3,
            "y": 4,
            "l_bumper": 5,
            "r_bumper": 6,
            "back": 7,
            "start": 8,
            "axis_l_trigger": 2,
            "axis_r_trigger": 3,
            "axis_l_stick_vert": 1,
            "axis_r_stick_vert": 5,  # TODO
            "axis_l_stick_horiz": 6,  # TODO
            "axis_r_stick_horiz": 4,
        }

        for item, number in items.items():
            if "axis" in item:
                setattr(
                    XBoxController, item, property(lambda self: self.getRawAxis(number))
                )
            else:
                self.__dict__[item] = JoystickButton(self, number)

