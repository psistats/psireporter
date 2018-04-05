#PsiReporter
PsiReporter is a basic framework for task execution and broadcasting the results. It's designed for simplicity and small scale usage.

## Usage
```py
from psireporter import OutputPlugin, ReporterPlugin, Manager
import time

class MyReporter(metaclass=ReporterPlugin):
    def report(self):
        return "this is a report"

class MyOutputter(metaclass=OutputPlugin):
    def send(self, report):
        print("Sending report: ", report)

if __name__ == "__main__":
    manager = Manager()
    manager.start()
    
    while True:
    	try:
	    time.sleep(1) 
	finally:
	    break

    manager.stop()
```

## Plugins

PsiReporter works with Reporter and Outputter plugins.

### ReporterPlugin

A Reporter plugin creates reports. 

To create a reporter plugin:

1. Create a class whose metaclass is `psireporter.ReporterPlugin`
2. Implement the method `report(self, config)`
3. Have this method return a value of some kind

#### Example

```py
import psireporter

class SimpleCounter(metaclass=psireporter.ReporterPlugin):
    def __init__(self):
        self.counter = 0
        
    def report(self, config):
        self.counter += 1
        return self.counter
```

### OutputterPlugin
