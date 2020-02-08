from inputs.xbox360 import XBoxController

from . import shooter
from . import indexer
from . import hopper

XBoxController().a.whenPressed(shooter.SetPercentage(1.0))
XBoxController().a.whenReleased(shooter.SetPercentage(0.0))

XBoxController().b.whenPressed(indexer.SetPercentage(1.0))
XBoxController().b.whenReleased(indexer.SetPercentage(0.0))

XBoxController().x.whenPressed(hopper.SetPercentage(1.0))
XBoxController().x.whenReleased(hopper.SetPercentage(0.0))
