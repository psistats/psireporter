from psireporter.plugin import Report
import pytest
import uuid
from unittest import mock
import datetime

def test_reportMutations():
    report = Report(message="foobar")

    with pytest.raises(AttributeError) as excinfo:
        report.id = "nope"

    with pytest.raises(AttributeError) as excinfo:
        report.timestamp = "nope"

    with pytest.raises(AttributeError) as excinfo:
        report.message = "nope"


def test_idGeneration():
    report = Report(message="foobar")

    id = uuid.UUID(report.id)

    assert str(id) == report.id

def test_timestamp():

    testdt = datetime.datetime(2016, 1, 1, 1, 1, 0, 0)

    with mock.patch('psireporter.plugin.datetime') as dt_mock:
        dt_mock.utcnow.return_value = testdt
        report = Report(message="foobar")

        assert report.timestamp == 1451610060

def test_settingValues():

    testdt = datetime.datetime(2016, 1, 1, 1, 1, 0 ,0)

    with mock.patch('psireporter.plugin.datetime') as dt_mock:
        dt_mock.utcnow.return_value = testdt

        report = Report(id="foo-id", message="foo-message")

        assert report.id == "foo-id"
        assert report.message == "foo-message"
        assert report.timestamp == 1451610060
