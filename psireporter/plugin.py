from psireporter.registry import Registry


class PluginMeta(type):
    """Base Plugin Metaclass

    Automatically assigns the attribute PLUGIN_ID if it does not
    exist, and adds it to the Registry.
    """
    def __init__(cls, pluginType, name, bases, namespaces):
        """Constructor

        :param cls: class Class to manipulate
        :param pluginType: str What type of plugin is it
        :param name: Name
        :param bases: Bases
        :param namespaces: Namespaces
        """
        super(PluginMeta, cls).__init__(name, bases, namespaces)

        if not hasattr(cls, 'PLUGIN_ID'):
            plugin_id = namespaces['__module__'] + '.' + namespaces['__qualname__']
        else:
            plugin_id = cls.PLUGIN_ID

        Registry.SetEntry(pluginType, plugin_id, cls)

    def __call__(cls, config=None, *args, **kwargs):
        """Meta istantiator

        Adds the config attribute to the instance. This means that the config
        attribute is not available in the class's constructor.

        :param config: object Configuration
        """
        instance = type.__call__(cls, *args, **kwargs)

        if config is None:
            setattr(instance, 'config', {})
        else:
            setattr(instance, 'config', config)

        return instance


class OutputPlugin(PluginMeta):
    """Output Plugin Metaclass"""
    def __init__(cls, name, bases, namespaces):
        super(OutputPlugin, cls).__init__("outputters", name, bases, namespaces)


class ReporterPlugin(PluginMeta):
    """Reporter Plugin Metaclass"""
    def __init__(cls, name, bases, namespaces):
        super(ReporterPlugin, cls).__init__("reporters", name, bases, namespaces)

