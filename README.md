# autonomous-drive-simulator

This is a simple and lightweight simulation engine to simulate the effects of multiple autonomous driving vehicles.

## usage

The tool is written in python and runs with
```bash
python main.py
```

With the following configuration it is possible to run it directly in visual studio code.

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python3",
            "type": "python",
            "request": "launch",
            "stopOnEntry": false,
            "console": "integratedTerminal",
            "pythonPath": "${config:python.pythonPath}",
            "program": "${workspaceRoot}/main.py",
            "cwd": "${workspaceRoot}",
            "env": {},
            "debugOptions": [
                "WaitOnAbnormalExit",
                "WaitOnNormalExit",
                "RedirectOutput"
            ]
        }
    ]
}
```

## libraries
The tool uses the following libraries
```python
import numpy 
import matplotlib
import random
import time
import math
```

