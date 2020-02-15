"""Module where commands are imported from and instantiated.

All Commands are Unique and should be accessed from the `command` module.

```python
from commands import shooter

shooter.SetPercentage(1.0).start()

# Or use the following if you are only working on the Shooter, for example.

from commands.shooter import SetPercentage

SetPercentage(1.0).start()
```
"""
from ctre import ControlMode

from inputs.xbox360 import XBoxController

from . import chassis, hopper, indexer, shooter, intake

XBoxController().a.whenPressed(shooter.ShooterSet(ControlMode.PercentOutput, 1.0))
XBoxController().a.whenReleased(shooter.ShooterSet(ControlMode.PercentOutput, 0.0))

XBoxController().b.whenPressed(indexer.IndexerSet(ControlMode.PercentOutput, 1.0))
XBoxController().b.whenReleased(indexer.IndexerSet(ControlMode.PercentOutput, 0.0))

XBoxController().x.whenPressed(hopper.HopperSet(ControlMode.PercentOutput, 1.0))
XBoxController().x.whenReleased(hopper.HopperSet(ControlMode.PercentOutput, 0.0))

XBoxController().y.whenReleased(intake.IntakeSet(ControlMode.PercentOutput, 1.0))
XBoxController().y.whenReleased(intake.IntakeSet(ControlMode.PercentOutput, 0.0))
