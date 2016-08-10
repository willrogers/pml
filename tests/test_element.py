import pkg_resources
from rml.exceptions import ConfigException
import rml.element
import pytest
import cothread
pkg_resources.require('cothread')


def test_create_element():
    e = rml.element.Element('BPM', 6.0)
    assert e.get_type() == 'BPM'
    assert e.get_length() == 6.0


def test_add_element_to_family():
    e = rml.element.Element('dummy', 0.0)
    e.add_to_family('fam')
    assert 'fam' in e.get_families()


def test_get_pv_value():
    PV = 'SR22C-DI-EBPM-04:SA:X'
    e = rml.element.Element('dummy', 0.0)
    e.set_pv('x', PV)
    print e.pv
    result = e.get_pv('x')
    assert isinstance(result, float)
    with pytest.raises(ConfigException):
        e.get_pv('y')
