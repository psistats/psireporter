from psireporter import OutputPlugin, ReporterPlugin, Manager
import time
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

class FastCounter(metaclass=ReporterPlugin):

    PLUGIN_ID = 'fast-counter'

    def __init__(self):
        self.counter = 0

    def report(self):
        self.counter += 1

        return 'fast count: %s' % self.counter


class SlowCounter(metaclass=ReporterPlugin):

    PLUGIN_ID = 'slow-counter'

    def __init__(self):
        self.counter = 0

    def report(self):
        self.counter += 1

        return 'slow count: %s' % self.counter


class Printer(metaclass=OutputPlugin):
    PLUGIN_ID = "my-printer"

    def __init__(self):
        self.logger = logging.getLogger('printer')

    def send(self, report):
        self.logger.info('Report: %s' % dict(report))


manager = Manager({
    'reporters': {
        'slow-counter': {
            'interval': 10
        },
        'fast-counter': {
            'interval': 1
        }
    }
})

manager.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    pass
finally:
    manager.stop()
