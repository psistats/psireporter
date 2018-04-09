from psireporter.worker import OutputWorker, OutputManager, ReporterManager

def test_sends_report():

    class TestOutput():
        def send(self, report):
            self.report = report

    to = TestOutput()

    ow = OutputWorker(to)

    ow.add_report('foobar')

    ow.tick()

    assert to.report == 'foobar'


def test_output_manager():

    class TestOutput():

        def __init__(self, config):
            pass

        def send(self, report):
            self.report = report


    class TestOutputTwo():
        def __init__(self, config):
            pass

        def send(self, report):
            self.report = report


    om = OutputManager((
        ('test-output-one', TestOutput),
        ('test-output-two', TestOutputTwo)
    ))

    om.add_report('test report')

    for w in om._workers:
        w.tick()
        assert w.outputter.report == 'test report'


def test_disabled_outputters():

    class EnabledOutputter():
        PLUGIN_ID = 'enabled-output'

        def __init__(self, config):
            self.reports = []

        def send(self, report):
            self.reports.append(report)

    class DisabledOutputter():
        PLUGIN_ID = 'disabled-output'

        def __init__(self, config):
            self.reports = []

        def send(self, report):
            self.reports.append(report)


    config = {
        'disabled-output': { 'enabled': False }
    }

    om = OutputManager((
        ('enabled-output', EnabledOutputter),
        ('disabled-output', DisabledOutputter)
    ), config)

    om.add_report('test report')

    assert len(om._workers) is 1

    for w in om._workers:
        w.tick()

    assert om._workers[0].outputter.reports[0] is 'test report'


def test_disabled_reporters():

    class ReporterOne():

        PLUGIN_ID = 'report-one'

        def __init__(self, config):
            pass

        def report(self):
            return 'enabled report'

    class ReporterTwo():

        PLUGIN_ID = 'report-two'

        def __init__(self, config):
            pass

        def report(self):
            return 'disabled report'


    class MockOutputManager():
        def __init__(self):
            self.reports = []

        def add_report(self, report):
            self.reports.append(report)

    config = {
        'report-one': {
            'interval': 1
        },
        'report-two': {
            'interval': 1,
            'enabled': False
        }
    }

    om = MockOutputManager()

    reports = (
        ('report-one', ReporterOne),
        ('report-two', ReporterTwo)
    )

    rm = ReporterManager(reports, om, config)

    rm.tick()

    assert om.reports[0].message == 'enabled report'
    assert len(om.reports) == 1


def test_reporter_manager():

    class ReporterOne():
        def __init__(self, config):
            pass

        def report(self):
            return 'report one'


    class ReporterTwo():
        def __init__(self, config):
            pass

        def report(self):
            return 'report two'

    class Outputter():
        def send(self, report):
            self.report = report

    class MockOutputManager():

        def __init__(self):
            self.reports = []

        def add_report(self, report):
            self.reports.append(report)


    config = {
        'reporter-two': {
            'interval': 3
        }
    }

    om = MockOutputManager()

    reporters = (
        ('reporter-one', ReporterOne),
        ('reporter-two', ReporterTwo)
    )

    rm = ReporterManager(reporters, om, config)

    # first tick, get  messages from each reporter
    rm.tick()

    assert len(om.reports) is 2

    assert om.reports[0].message == 'report one'
    assert om.reports[0].sender == 'reporter-one'

    assert om.reports[1].message == 'report two'
    assert om.reports[1].sender == 'reporter-two'

    # second tick, get messages from first reporter
    rm.tick()

    assert len(om.reports) == 3
    assert om.reports[2].message == 'report one'
    assert om.reports[2].sender == 'reporter-one'

    # third tick, get messages from all reporters
    rm.tick()

    assert len(om.reports) == 5
    assert om.reports[3].message == 'report one'
    assert om.reports[3].sender == 'reporter-one'
    assert om.reports[4].message == 'report two'
    assert om.reports[4].sender == 'reporter-two'

    # fourth tick, get messages from first reporter
    rm.tick()

    assert len(om.reports) == 6
    assert om.reports[5].message == 'report one'
    assert om.reports[5].sender == 'reporter-one'

    # fifth tick, get messages from first reporter
    rm.tick()
    assert len(om.reports) == 7
    assert om.reports[6].message == 'report one'
    assert om.reports[6].sender == 'reporter-one'

    # sixth tick, get messages from all reporters
    rm.tick()
    assert len(om.reports) == 9
    assert om.reports[7].message == 'report one'
    assert om.reports[7].sender == 'reporter-one'
    assert om.reports[8].message == 'report two'
    assert om.reports[8].sender == 'reporter-two'


