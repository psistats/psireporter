import uuid
from datetime import datetime
import calendar
from psireporter.registry import Registry

class PluginError(Exception):
    def __init__(self, message):
        super().__init__(message)

class OutputterPlugin(type):
    def __init__(cls, name, bases, namespaces):
        super(OutputterPlugin, cls).__init__(name, bases, namespaces)
        Registry.SetEntry("outputters", cls.ID, cls)


class ReporterPlugin(type):
    def __init__(cls, name, bases, namespaces):

        if not hasattr(cls, "ID"):
            raise PluginError("Missing class attribute ID")

        if not hasattr(cls, "report"):
            raise PluginError("Reporter plugins must implement the method 'report'")

        super(ReporterPlugin, cls).__init__(name, bases, namespaces)
        Registry.SetEntry("reporters", cls.ID, cls)



class Plugin():
    """Base Plugin Class"""
    pass


class OutputPlugin(Plugin):
    """Output Plugin Class

    Extend this class for plugins that send reports"""

    def __init__(self, config):
        self.config = config

    def send(self, report):
        raise NotImplementedError


class ReporterPlugin(Plugin):
    """Report Plugin Class

    Extend this class for plugins that generate reports"""

    def __init__(self, config):
        self.config = config

    def report(self):
        raise NotImplementedError()

class PluginConfig():
    def __init__(self, *args, **kwargs):
        self._interval = kwargs.get('interval', 1)
        self._enabled = kwargs.get('enabled', True)

        if self._enabled == "true":
            self._enabled = True
        elif self._enabled == "false":
            self._enabled = False

        self._properties = {}

        for propName in kwargs:
            self._properties[propName] = kwargs.get(propName)


    def __getattr__(self, k):
        if k in self._properties:
            return self._properties[k]
        else:
            raise AttributeError("%s is not defined" % k)


class Report():

    def __init__(self, *args, **kwargs):
        self._id = kwargs.get('id', None)

        if self._id == None:
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
