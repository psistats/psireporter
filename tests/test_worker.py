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
        def send(self, report):
            self.report = report


    class TestOutputTwo():
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


def test_reporter_manager():

    class ReporterOne():
        def report(self, config):
            return 'report one'


    class ReporterTwo():
        def report(self, config):
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
        'reporters': {
            'reporter-two': {
                'interval': 3
            }
        }
    }

    om = MockOutputManager()

    reporters = (
        ('reporter-one', ReporterOne),
        ('reporter-two', ReporterTwo)
    )

    rm = ReporterManager(reporters, om, config)

    rm.tick()
    rm.tick()
    rm.tick()

    assert rm._counter == 4

    assert om.reports[0].message == 'report one'
    assert om.reports[0].sender == 'reporter-one'

    assert om.reports[1].message == 'report one'
    assert om.reports[1].sender == 'reporter-one'

    assert om.reports[2].message == 'report one'
    assert om.reports[2].sender == 'reporter-one'

    assert om.reports[3].message == 'report two'
    assert om.reports[3].sender == 'reporter-two'

    rm.tick()

    assert rm._counter == 2
    assert om.reports[4].message == 'report one'
    assert om.reports[4].sender == 'reporter-one'

