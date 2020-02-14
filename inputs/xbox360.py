from wpilib import Joystick
from wpilib.buttons import JoystickButton

from fusion.unique import unique


@unique
class XBoxController(Joystick):
    def __init__(self, port: int = 0):
        super().__init__(port)

        self.items = {
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

        # Adds attributes based on items
        for item, number in self.items.items():
            if "axis" in item:
                setattr(self, item, lambda self: self.getRawAxis(number))
            else:
                self.__dict__[item] = JoystickButton(self, number)

    def __getattr__(self, name):
        # Overloaded very jankily, but this works well
        if f"axis_{name}" in list(filter(lambda i: "axis" in i, self.items.keys())):
            return object.__getattribute__(self, f"axis_{name}")(self)
        return object.__getattribute__(self, name)
