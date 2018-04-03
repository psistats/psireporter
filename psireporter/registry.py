class RegistryError(Exception):
    def __init__(self, message):
        super().__init__(message)


class RegistryDuplicateError(RegistryError):
    def __init__(self, message):
        super().__init__(message)


class RegistryKeyError(RegistryError):
    def __init__(self, message):
        super().__init__(message)


class Registry():
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
    def GetRegistry(regname):
        if regname not in Registry.__instances:
            Registry.__instances[regname] = Registry.__Registry(regname)
        return Registry.__instances[regname]

    @staticmethod
    def GetEntry(regname, entryName):
        reg = Registry.GetRegistry(regname)
        return reg.get(entryName)

    @staticmethod
    def SetEntry(regname, entryName, entry):
        reg = Registry.GetRegistry(regname)
        reg.set(entryName, entry)

    @staticmethod
    def GetEntries(regname):
        reg = Registry.GetRegistry(regname)
        return reg.entries()

    @staticmethod
    def Clear(regname):
        reg = Registry.GetRegistry(regname)
        reg.clear()

    @staticmethod
    def HasEntry(regname, entryName):
        reg = Registry.GetRegistry(regname)
        return reg.has(entryName)

    @staticmethod
    def ClearAll():
        Registry.__instances = {}
