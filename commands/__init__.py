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
from inputs.xbox360 import XBoxController

from . import chassis, hopper, indexer, shooter

XBoxController().a.whenPressed(shooter.SetPercentage(1.0))
XBoxController().a.whenReleased(shooter.SetPercentage(0.0))

XBoxController().b.whenPressed(indexer.SetPercentage(1.0))
XBoxController().b.whenReleased(indexer.SetPercentage(0.0))

XBoxController().x.whenPressed(hopper.SetPercentage(1.0))
XBoxController().x.whenReleased(hopper.SetPercentage(0.0))
