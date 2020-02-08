"""
This module contains all subsystem functionality.

NOTE: All Subsystems are Singleton classes. The best way to get an
instance of a Subsystem is by using the class constructor, which
will return the existing instance.

```python
chassis_instance = Chassis()
chassis_instance_again = Chassis()

assert chassis_instance is chassis__instance_again
```
"""

from .chassis import *
from .indexer import *
from .intake import *
from .lift import *
from .shooter import *
from .hopper import *
