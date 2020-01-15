from math import *


def velocity_calculator(v_rob, theta, distance, height):
    velocity = (
        2 * v_rob * cos(theta)
        - v_rob * sin(theta) * distance
        + sqrt(
            (2 * v_rob * cos(theta) - v_rob * sin(theta) * distance) ** 2
            + 4
            * (sin(theta) * cos(theta) * distance - height * cos(theta) ** 2)
            * (9.8 * distance ** 2 / 2 + v_rob ** 2)
        )
    ) / (2 * (sin(theta) * cos(theta) * distance - height * cos(theta) ** 2))
    return velocity
