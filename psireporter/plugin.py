import uuid
from datetime import datetime
import calendar


class RegisterPlugin():
    def __init__(self, plugin_id, plugin_name, plugin_type):
        self.plugin_id = plugin_id
        self.plugin_name = plugin_name
        self.plugin_type = plugin_type

    def __call__(self, cls, *args, **kwargs):
        setattr(cls, "PLUGIN_ID", self.plugin_id)
        setattr(cls, "PLUGIN_TYPE", self.plugin_type)

        PluginRegistry.Get().add_plugin(cls)

        return cls


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
