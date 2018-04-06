import uuid
from datetime import datetime
import calendar
from psireporter.registry import Registry


class PluginMeta(type):
    def __init__(cls, pluginType, name, bases, namespaces):
        super(PluginMeta, cls).__init__(name, bases, namespaces)

        if not hasattr(cls, 'PLUGIN_ID'):
            plugin_id = namespaces['__module__'] + '.' + namespaces['__qualname__']
        else:
            plugin_id = cls.PLUGIN_ID

        Registry.SetEntry(pluginType, plugin_id, cls)


class OutputPlugin(PluginMeta):
    def __init__(cls, name, bases, namespaces):
        super(OutputPlugin, cls).__init__("outputters", name, bases, namespaces)


class ReporterPlugin(PluginMeta):
    def __init__(cls, name, bases, namespaces):
        super(ReporterPlugin, cls).__init__("reporters", name, bases, namespaces)

