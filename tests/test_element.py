import pkg_resources
from rml.exceptions import PvUnknownHandleError, PvUnknownFieldError
import rml.element
import pytest
import cothread
pkg_resources.require('cothread')


def get_elements(fields):
    # Return a list of requested elements
    # <list> fields: 'x' or 'y'
    result = list()
    if 'x' in fields:
        pv_x = 'SR22C-DI-EBPM-04:SA:X'
        e = rml.element.Element('dummy_x', 0.0, cs='epics')
        e.set_pv('x', pv_x)
        result.append(e)
    if 'y' in fields:
        pv_y = 'SR22C-DI-EBPM-04:SA:Y'
        e = rml.element.Element('dummy_y', 0.0, cs='epics')
        e.set_pv('y', pv_y)
        result.append(e)
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
    pv = get_elements(['x', 'y'])
    assert isinstance(pv[0].get_pv('x'), float)
    assert isinstance(pv[1].get_pv('y'), float)


def test_get_pv_exceptions():
    pvs = get_elements(['x', 'y'])
    with pytest.raises(PvUnknownFieldError):
        pvs[0].get_pv('unknown_field')
    with pytest.raises(PvUnknownHandleError):
        pvs[1].get_pv('y', 'unkown_handle')
