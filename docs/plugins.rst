Plugins
*******

PsiReporter plugins are divided into two different types, Reporters and Outputters.

Reporters generate reports and Outputters send those reports places. The Manager thread
coordinates executing reporters and queuing the resulting reports with a list of output
plugins.

Plugin Types
============

Reporters
---------

To create a reporter plugin:

1. Create a class whose metaclass is :class:`psireporter.ReporterPlugin`
2. Implement the method `report(self)`

.. code-block:: python

  import psireporter

  class SimpleCounter(metaclass=psireporter.ReporterPlugin):
    def __init__(self):
      self.counter = 0

    def report(self):
      self.counter += 1
      return self.counter

By using the metaclass :class:`psireporter.ReporterPlugin` your plugin will be automatically
registerd in the plugin registry.

If your reporter requires some configuration, the attribute 'config' is set automatically after
the class is constructed. For example:

.. code-block:: python

  import psireporter

  class SimpleCounter(metaclass=psireporter.ReporterPlugin):
    def __init__(self):
      self.counter = 0

    def report(self):
      self.counter += self.config['steps']
      return self.counter

Outputters
----------

To create an output plugin:

1. Create a class whose metaclass is :class:`psireporter.OutputPlugin`
2. Implement the method `output(self, report)`

.. code-block:: python

  import psireporter

  class BasicPrinter(metaclass=psireporter.OutputPlugin):
    def send(self, report):
      print('Message ID: %s - Sender: %s - Timestamp: %s - Message: %s' % (
        report.id,
        report.sender,
        report.timestamp,
        report.message
      ))

Like reporters, a config object is made available after construction. Because you can not
access the configuration object in the constructor, you may need to perform some logic
to initialize your plugin in the `send(self, report)` method.

.. code-block:: python

  import psireporter
  import socket
  import json

  class BasicNetworkSender(metaclass=psireporter.OutputPlugin):
    def __init__(self):
      self.initialized = False

    def init(self):
      self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self._sock.connect((self.config['ip'], self.config['port']))
      self.initialized = True

    def send(self, report):
      if self.initialized is False:
        self.init()
      self._sock.send(json.dumps(dict(report)))
 
.. warning::
  There is no way currently to clean up a plugin. Thus in this example, there
  is no chance for you to call self._sock.close(). This feature is in development.


