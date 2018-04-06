import threading
import time
import collections
import logging
from datetime import datetime
import uuid
import calendar
from psireporter.registry import Registry
import json

class Report():

    def __init__(self, **kwargs):
        self._id = kwargs.get('id', None)

        if self._id is None:
            self._id = str(uuid.uuid1())

        self._message = kwargs.get('message', None)

        d = datetime.utcnow()
        unixtime = calendar.timegm(d.utctimetuple())
        self._timestamp = unixtime

    @property
    def id(self):
        return self._id

    @property
    def message(self):
        return self._message

    @property
    def timestamp(self):
        return self._timestamp

    def __str__(self):
        return 'RID: %s - TS: %s - MSG: %s' % (self._id, self._message, self._timestamp)

    def __repr__(self):
        return json.dumps({
            'id': self._id,
            'ts': self._timestamp,
            'msg': self._message
        })



class Manager(threading.Thread):
    def __init__(self, config, *args, **kwargs):

        self.logger = logging.getLogger(name='psireporter.manager')

        self.running = False
        self.config = config
        super().__init__(*args, **kwargs)

    def start(self):
        self.running = True
        super().start()

    def stop(self):
        self.running = False

    def run(self):

        self.logger.info('Start manager threads')
        outputters = Registry.GetEntries('outputters')
        reporters = Registry.GetEntries('reporters')

        o_manager = OutputManager(outputters, self.config)
        r_manager = ReporterManager(reporters, self.config, o_manager)

        o_manager.start()
        r_manager.start()

        while self.running is True:
            time.sleep(5)

        o_manager.stop()
        r_manager.stop()

        self.logger.info('Stopped')


class OutputWorker(threading.Thread):
    def __init__(self, outputter, *args, **kwargs):
        self.logger = logging.getLogger(name='psireporter.output-worker')
        self.report_queue = collections.deque()
        self.running = False
        self.outputter = outputter
        super().__init__(*args, **kwargs)

    def start(self):
        self.running = True
        super().start()

    def stop(self):
        self.running = False

    def add_report(self, report):
        self.report_queue.append(report)

    def tick(self):
        if len(self.report_queue) > 0:
            report = self.report_queue.popleft()
            self.outputter.send(report)
        else:
            time.sleep(1)

    def run(self):

        while self.running is True:
            self.tick()

        self.logger.info(self.outputter.__class__.__name__ + ' stopped')


class OutputManager(threading.Thread):
    def __init__(self, outputters, config, *args, **kwargs):
        self.logger = logging.getLogger(name='psireporter.output-manager')
        self._workers = []

        if config is None:
            self.config = {
                "outputters": {}
            }

        for outputter_id, outputter in outputters:
            self._workers.append(OutputWorker(outputter()))

        super().__init__(*args, **kwargs)

    def start(self):
        self.running = True
        super().start()

    def stop(self):
        self.running = False

    def add_report(self, report):
        for worker in self._workers:
            worker.add_report(report)

    def has_running_workers(self):
        for worker in self._workers:
            if worker.running is True:
                return True
        return False

    def run(self):

        for worker in self._workers:
            worker.start()

        while self.running is True:
            time.sleep(10)

        for worker in self._workers:
            worker.stop()

        while self.has_running_workers():
            time.sleep(10)

        self.logger.info('Stopped')


class ReporterManager(threading.Thread):

    def __init__(self, reporters, config, o_manager, *args, **kwargs):

        self.logger = logging.getLogger('psireporter.reporter-manager')

        if config is None:
            self.config = {
                "reporters": {}
            }
        else:
            self.config = config

        self.running = False
        self._o_manager = o_manager

        self._reporter_counter = 0
        self._max_reporter_counter = 0

        self._reporters = {}
        self._outputters = {}
        self._triggers = {}
        self._counter = 1

        for reporter_id, reporter in reporters:
            self._reporters[reporter_id] = reporter()

            if reporter_id not in self.config["reporters"]:
                self.config["reporters"][reporter_id] = {
                    'interval': 1,
                    'settings': {}
                }
            else:
                if 'interval' not in self.config['reporters'][reporter_id]:
                    self.config['reporters'][reporter_id]['interval'] = 1

                if 'settings' not in self.config['reporters'][reporter_id]:
                    self.config['reporters'][reporter_id]['settings'] = {}

            interval = self.config['reporters'][reporter_id]['interval']

            if interval not in self._triggers:
                self._triggers[interval] = []

            self._triggers[interval].append(reporter_id)

        self._max_reporter_counter = max(self._triggers.keys())

        self._trigger_counters = self._triggers.keys()

        super().__init__(*args, **kwargs)

    def start(self):
        self.running = True
        super().start()

    def stop(self):
        self.running = False

    def tick(self):
        if self._counter > self._max_reporter_counter:
            self._counter = 1

            for counter in self._trigger_counters:
                if self._counter % counter == 0:
                    for reporter_id in self._triggers[counter]:
                        reporter = self._reporters[reporter_id]
                        message = reporter.report(None)

                        report = Report(id=reporter_id, message=message)

                        self._o_manager.add_report(report)
        self._counter += 1
        time.sleep(1)

    def run(self):

        self.logger.info('Starting')
        self.logger.debug('Max counter: %s' % self._max_reporter_counter)
        self.logger.debug('Triggers: %s' % self._triggers)

        while self.running is True:
            self.tick()

        self.logger.info('Stopped')
