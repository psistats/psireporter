Basic Usage
***********

In this basic example, you create a counter that will increment every second, an output plugin that simply outputs the report to stdout.

.. code-block:: python

  import time
  from psireporter import OutputPlugin, ReporterPlugin, Manager

  class ExampleCounter(metaclass=ReporterPlugin):
      def __init__(self):
          self.counter = 0

      def report(self):
          self.counter += 1
          return self.counter

  class StdoutPlugin(metaclass=OutputPlugin):
      def send(self, report):
          print(report.message)

  manager = Manager()
  manager.start()
 
  while True:
     try:
       time.sleep(1)
     except KeyboardInterrupt:
       break

  manager.stop()

