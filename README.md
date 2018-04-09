# PsiReporter
PsiReporter is a basic framework for multithreaded task execution and 
broadcasting the results. It's designed for simplicity and small scale usage.

For more information visit http://psireporter.readthedocs.io/en/develop/usage.html

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
2. Implement the method `report(self)`
3. Have this method return a value of some kind

#### Example

```py
import psireporter

class SimpleCounter(metaclass=psireporter.ReporterPlugin):
  def __init__(self):
    self.counter = 0
        
  def report(self):
    self.counter += 1
    return self.counter
```

### OutputterPlugin

An output plugin sends a report somewhere.

To create an output plugin:

1. Create a class whose metaclass is `psirpoerter.OutputPlugin`
2. Implement the method `send(self, report)`

#### Example

```py
import psireporter

class SimplePrinter(metaclass=psireporter.ReporterPlugin):
  def send(self, report):
    print(dict(report))
```

### Report Object

While Report plugins don't need to return anything other than their own data, that data is then wrapped into an immutable Report object.
