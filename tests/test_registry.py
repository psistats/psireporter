from psireporter.registry import Registry, RegistryDuplicateError, RegistryKeyError, RegistryError
import pytest

def test_add_entry():

    Registry.SetEntry("testreg1", "testent1", "entry")

    assert Registry.GetEntry("testreg1", "testent1") == "entry"

def test_bad_key():
    
    with pytest.raises(RegistryKeyError) as excinfo:
        entry = Registry.GetEntry("testreg", "foobar")


def test_duplicate_key():
    with pytest.raises(RegistryDuplicateError) as excinfo:
        Registry.SetEntry("testreg5", "foo", "bar")
        Registry.SetEntry("testreg5", "foo", "foo")


def test_clear_registry():

    Registry.SetEntry("testreg2", "testent2", "entry")
    Registry.SetEntry("testreg2", "testent3", "entry2")

    Registry.Clear("testreg2")

    with pytest.raises(RegistryKeyError) as excinfo:
        entry = Registry.GetEntry("testreg2", "testent2")

    with pytest.raises(RegistryKeyError) as excinfo:
        entry = Registry.GetEntry("testreg2", "testent3")


def test_clear_all():

    Registry.SetEntry("testreg3", "testent1", "entry")
    Registry.SetEntry("testreg4", "testent2", "entry")

    Registry.ClearAll()

    with pytest.raises(RegistryKeyError) as excinfo:
        entry = Registry.GetEntry("testreg3", "testent1")

    with pytest.raises(RegistryKeyError) as excinfo:
        entry = Registry.GetEntry("testreg4", "testent2")


def test_immutable_regname():
    reg = Registry.GetRegistry("another-registry")

    assert reg.regname == "another-registry"

    with pytest.raises(AttributeError) as excinfo:
        reg.regname = "foobar"


def test_block_instantiation():
    with pytest.raises(RegistryError) as excinfo:
        reg = Registry()

def test_get_entries():

    Registry.ClearAll()
    Registry.SetEntry("some-registry", "foo", "bar")
    Registry.SetEntry("some-registry", "hello", "world")
   
    assert Registry.GetEntries("some-registry") == (("foo", "bar"), ("hello", "world"),)