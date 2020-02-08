from inputs.xbox360 import XBoxController

from . import shooter

XBoxController().a.whenPressed(shooter.SetPercentage(1.0))
XBoxController().b.whenPressed(shooter.SetPercentage(0.0))
