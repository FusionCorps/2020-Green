"""
This module contains all subsystem functionality and instances.

All Subsystems are Singletons, meaning only one instance of that class may
exist at a time. The preferred way of accessing Subsystem instances is
importing the Subsystem class from the `subsystem` module then use
constructor notation to fetch the instance.

```python
from subsystems import Indexer

Indexer().do_something()
```
"""

from .chassis import *
from .hopper import *
from .indexer import *
from .intake import *
from .lift import *
from .shooter import *
