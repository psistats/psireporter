import threading
import time
import collections
import asyncio

class ReporterWorker(threading.Thread):

    def __init__(self, reporter, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.running = False
        self.reporter = reporter

    def start(self):
        self.running = True
        super().start()

    def run(self):
        while (self.running):
            time.sleep(self.reporter.config.interval)

    def stop(self):
        self.running = False

class OutputManager(threading.Thread):
    """Output Manager

    Manages output threads."""
    def __init__(self, outputters, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.running = False
        self._workers = []
        self._reports = collections.deque()
        self.outputters = outputters

    def start(self, *args, **kwargs):

        for outputter in self.outputters:
            self._workers.append(OutputWorker(outputter))

        self.running = True

        super().start(*args, **kwargs)

    def add_report(self, report):
        self._reports.append(report)

    def run(self):

        for worker in self._workers:
            worker.start()

        while self.running is True:
            if len(self._reports) > 0:
                report = self._reports.popleft()
                for worker in self._workers:
                    worker.add_report(report)
                time.sleep(0.01)
            else:
                time.sleep(5)

        for worker in self._workers:
            worker.stop()

    def stop(self):
        self.running = False


class OutputWorker(threading.Thread):
    """Output Worker

    Runs an outputter plugin in a thread"""
    def __init__(self, outputter, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.running = False
        self.config = {}
        self.outputter = outputter
        self._reports = collections.deque()


    def add_report(self, report):
        self._reports.append(report)


    def start(self):
        self.running = True
        super().start()


    def run(self):
        while self.running is True:
            if (len(self._reports) >= 1):
                report = self._reports.popleft()
                self.outputter.send(report)
            else:
                time.sleep(1)

        print("Outputter worker thread finished")


    def stop(self):
        self.running = False
