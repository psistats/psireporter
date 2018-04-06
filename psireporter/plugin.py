from psireporter.registry import Registry


class PluginMeta(type):
    def __init__(cls, pluginType, name, bases, namespaces):
        super(PluginMeta, cls).__init__(name, bases, namespaces)

        if not hasattr(cls, 'PLUGIN_ID'):
            plugin_id = namespaces['__module__'] + '.' + namespaces['__qualname__']
        else:
            plugin_id = cls.PLUGIN_ID

        Registry.SetEntry(pluginType, plugin_id, cls)

    def __call__(cls, config=None, *args, **kwargs):

        instance = type.__call__(cls, *args, **kwargs)

        if config is None:
            setattr(instance, 'config', {})
        else:
            setattr(instance, 'config', config)

        return instance


class OutputPlugin(PluginMeta):
    def __init__(cls, name, bases, namespaces):
        super(OutputPlugin, cls).__init__("outputters", name, bases, namespaces)


class ReporterPlugin(PluginMeta):
    def __init__(cls, name, bases, namespaces):
        super(ReporterPlugin, cls).__init__("reporters", name, bases, namespaces)

