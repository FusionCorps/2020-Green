from inputs.xbox360 import XBoxController

from . import shooter

XBoxController().a.whenPressed(shooter.SetPercentage(1.0))
XBoxController().a.whenReleased(shooter.SetPercentage(0.0))
