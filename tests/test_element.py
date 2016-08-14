import pkg_resources
from rml.exceptions import PvUnknownHandleError, PvUnknownFieldError
import rml.element
import rml.dummycontrolsystem
import pytest
pkg_resources.require('cothread')


@pytest.fixture
def get_elements(fields):
    # Return a list of requested elements
    # <list> fields: 'x' or 'y'
    dummy_control_system = rml.dummycontrolsystem.DummyControlSystem()
    result = dict()
    if 'x' in fields:
        pv_x = 'SR22C-DI-EBPM-04:SA:X'
        e = rml.element.Element('dummy_x', 0.0, cs=dummy_control_system)
        e.put_pv_name('x', pv_x)
        result['x'] = e
    if 'y' in fields:
        pv_y = 'SR22C-DI-EBPM-04:SA:Y'
        e = rml.element.Element('dummy_y', 0.0, cs=dummy_control_system)
        e.put_pv_name('y', pv_y)
        result['y'] = e
    return result


def test_create_element():
    e = rml.element.Element('BPM', 6.0)
    assert e.get_type() == 'BPM'
    assert e.get_length() == 6.0


def test_add_element_to_family():
    e = rml.element.Element('dummy', 0.0)
    e.add_to_family('fam')
    assert 'fam' in e.get_families()


def test_get_pv_value():
    pvs = get_elements(['x', 'y'])
    assert isinstance(pvs['x'].get_pv_value('x'), float)
    assert isinstance(pvs['y'].get_pv_value('y'), float)


def test_get_pv_exceptions():
    pvs = get_elements(['x', 'y'])
    with pytest.raises(PvUnknownFieldError):
        pvs['x'].get_pv_value('unknown_field')
    with pytest.raises(PvUnknownHandleError):
        pvs['y'].get_pv_value('y', 'unkown_handle')
