Advanced Usage
--------------

In this example, we configure a reporter to execute every five seconds, and to increment at a configured rate. As well, we setup an output plugin to print the counter, but with a configurable prefix.

.. code-block:: python

  import time
  from psireporter import OutputPlugin, ReporterPlugin, Manager
  
  class ExampleCounter(metaclass=ReporterPlugin):

    PLUGIN_ID = 'example_counter'

    def __init__(self):
      self.counter = 0

    def report(self):
      self.counter += self.config['rate']
      return self.counter

  class StdoutPlugin(metaclass=OutputPlugin):

    PLUGIN_IN = 'stdout'

    def send(self, report):
      print('%s: %s' % (self.config['prefix'], report.message))

  
  conf = {
    'reporters': {
      'example_counter': {
        'interval': 5,
        'settings': {
          'rate': 3
        }
      }
    },
    'outputters': {
      'stdout': {
        'settings': {
          'prefix': 'example'
        }
      }
    }
  }

  manager = Manager(conf)
  manager.start()

  while True:
    try:
      time.sleep(1)
    except KeyboardInterrupt:
      break

  manager.stop()

