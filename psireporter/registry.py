class RegistryError(Exception):
    """Base exception class for registry errors"""
    def __init__(self, message):
        super().__init__(message)


class RegistryDuplicateError(RegistryError):
    """Raises when setting a key that already exists"""
    def __init__(self, message):
        super().__init__(message)


class RegistryKeyError(RegistryError):
    """Raised when accessing a key that does not exist"""
    def __init__(self, message):
        super().__init__(message)


class Registry():
    """Registry

    The registry is a basic singleton to key/value pairs.

    Values can be anything, including dictionaries and lists.

    :Example:

    Registry.SetEntry('root', 'foo', 'bar')
    Registry.GetEntry('root', 'foo')

    You can also get a registry for a specific name:

    :Example:

    reg = Registry.GetRegisry('root')
    reg.set('foo', 'bar')
    reg.get('foo')

    """
    class __Registry():
        def __init__(self, regname):
            self._regname = regname
            self._entries = {}

        @property
        def regname(self):
            return self._regname

        def set(self, entryName, entry):
            if entryName in self._entries:
                raise RegistryDuplicateError("Entry %s already exists" % entryName)
            self._entries[entryName] = entry

        def get(self, entryName):
            if entryName not in self._entries:
                raise RegistryKeyError("Entry %s does not exist" % entryName)
            return self._entries[entryName]

        def has(self, entryName):
            if entryName not in self._entries:
                return False
            return True

        def entries(self):
            return tuple(self._entries.items())

        def clear(self):
            self._entries = {}

    __instances = {}

    def __init__(self):
        raise RegistryError("Can not instantiate registry directly, use Registry.Get(regname)")

    @staticmethod
    def GetRegistry(registry_name):
        """Get a registry for the specific registry name"""
        if registry_name not in Registry.__instances:
            Registry.__instances[registry_name] = Registry.__Registry(registry_name)
        return Registry.__instances[registry_name]

    @staticmethod
    def GetEntry(registry_name, entry):
        """Get an entry for a specific registry"""
        reg = Registry.GetRegistry(registry_name)
        return reg.get(entry)

    @staticmethod
    def SetEntry(registry_name, entry, value):
        """Set an entry for a specific registry"""
        reg = Registry.GetRegistry(registry_name)
        reg.set(entry, value)

    @staticmethod
    def GetEntries(registry_name):
        """Get all entries of a specific registry"""
        reg = Registry.GetRegistry(registry_name)
        return reg.entries()

    @staticmethod
    def Clear(registry_name):
        """Clear all entries of a specific registry"""
        reg = Registry.GetRegistry(registry_name)
        reg.clear()

    @staticmethod
    def HasEntry(registry_name, entry):
        """Check to see if an entry exists in a specific registry"""
        reg = Registry.GetRegistry(registry_name)
        return reg.has(entry)

    @staticmethod
    def ClearAll():
        """Deletes ALL existing registries"""
        Registry.__instances = {}
