import pkg_resources
from rml.exceptions import PvUnknownHandleError, PvUnknownFieldError
import rml.element
import dummycontrolsystem
import pytest
pkg_resources.require('cothread')


@pytest.fixture
def get_elements(fields):
    # Return a list of requested elements
    # <list> fields: 'x' or 'y'
    dummy_control_system = dummycontrolsystem.DummyControlSystem()
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
    e = rml.element.Element(4, 'BPM', length=6.0)
    assert 'BPM' in e.families
    assert e.length == 6.0


def test_add_element_to_family():
    e = rml.element.Element('dummy', 0.0)
    e.add_to_family('fam')
    assert 'fam' in e.families


def test_get_set_pv_value():
    # Tests to get/set pv names and/or values
    pvs = get_elements(['x', 'y'])
    assert isinstance(pvs['x'].get_pv_value('x'), float)
    assert isinstance(pvs['y'].get_pv_value('y'), float)
    pvs['x'].put_pv_value('x', 4)
    assert pvs['x'].get_pv_value('x') == 4


def test_get_pv_exceptions():
    pvs = get_elements(['x', 'y'])
    with pytest.raises(PvUnknownFieldError):
        pvs['x'].get_pv_value('unknown_field')
    with pytest.raises(PvUnknownHandleError):
        pvs['y'].get_pv_value('y', 'unkown_handle')
