import pkg_resources
from rml.exceptions import PvException
import rml.element
import dummycontrolsystem
from rml.unitconversion import UnitConversion
import pytest
pkg_resources.require('cothread')


@pytest.fixture
def get_elements(handle, fields, unit_conversion=UnitConversion([1, 0])):
    # Return a list of requested elements
    # <list> fields: 'x' or 'y'
    dummy_control_system = dummycontrolsystem.DummyControlSystem()
#    dummy_control_system.get = mock.MagicMock(return_value=4)
#    self._cs.get('duumy')
#    dummy_control_system.get.assert_called_with('dummy')
#    dummy_control_system.set.assert_called_with(pv, value)
    result = dict()
    if 'x' in fields:
        pv_x = 'SR22C-DI-EBPM-04:SA:X'
        e = rml.element.Element('dummy_x', length=0.0, cs=dummy_control_system,
                                uc=unit_conversion)
        e.put_pv_name(handle, 'x', pv_x)
        if handle == 'setpoint':
            e.put_pv_value('x', 0.0, unit='machine')
        result['x'] = e
    if 'y' in fields:
        pv_y = 'SR22C-DI-EBPM-04:SA:Y'
        e = rml.element.Element('dummy_y', length=0.0, cs=dummy_control_system,
                                uc=unit_conversion)
        e.put_pv_name(handle, 'y', pv_y)
        if handle == 'setpoint':
            e.put_pv_value('y', 0.0, unit='machine')
        result['y'] = e
    return result


def test_create_element():
    e = rml.element.Element(4, length=6.0)
    e.add_to_family('BPM')
    assert 'BPM' in e.families
    assert e.length == 6.0


def test_add_element_to_family():
    e = rml.element.Element('dummy')
    e.add_to_family('fam')
    assert 'fam' in e.families


def test_readback_pvs():
    # Tests to get/set pv names and/or values
    pvs = get_elements('readback', ['x', 'y'])
    assert isinstance(pvs['x'].get_pv_value('readback', 'x'), float)
    assert isinstance(pvs['y'].get_pv_value('readback', 'y'), float)
    assert isinstance(pvs['x'].get_pv_name('readback'), dict)
    assert isinstance(pvs['y'].get_pv_name('readback', 'y'), str)


def test_setpoint_pvs():
    pvs = get_elements('setpoint', ['x', 'y'])
    assert isinstance(pvs['x'].get_pv_value('setpoint', 'x'), float)
    assert isinstance(pvs['y'].get_pv_value('setpoint', 'y'), float)
    assert isinstance(pvs['x'].get_pv_name('setpoint'), dict)
    assert isinstance(pvs['y'].get_pv_name('setpoint', 'y'), str)

    pvs['x'].put_pv_value('x', 4)
    assert pvs['x'].get_pv_value('setpoint', 'x') == 4


def test_get_pv_exceptions():
    pvs = get_elements('setpoint', ['x', 'y'])
    with pytest.raises(PvException):
        pvs['x'].get_pv_value('setpoint', 'unknown_field')
    with pytest.raises(PvException):
        pvs['y'].get_pv_value('unknown_handle', 'y')

    with pytest.raises(PvException):
        pvs['x'].get_pv_name('unknown_handle')


def test_put_pv_exceptions():
    pvs = get_elements('setpoint', ['x', 'y'])
    with pytest.raises(PvException):
        pvs['x'].put_pv_value('unknown_field', 4.0)
    with pytest.raises(PvException):
        pvs['y'].put_pv_name('unknown_handle', 'x',
                             'SR21C-DI-EBPM-04:SA:Y')


def test_identity_conversion():
    # Test identity unit conversion
    identity_conversion = UnitConversion([1, 0])
    pvs = get_elements('setpoint', ['x', 'y'],
                       unit_conversion=identity_conversion)
    pvs['x'].put_pv_value('x', 4.0, unit='machine')
    pvs['y'].put_pv_value('y', 4.0, unit='physics')
    value_physics = pvs['x'].get_pv_value('setpoint', 'x', 'physics')
    value_machine = pvs['y'].get_pv_value('setpoint', 'y', 'machine')
    assert value_physics == 4.0
    assert value_machine == 4.0


def test_linear_conversion():
    # Test linear unit conversion
    linear_conversion = UnitConversion([2, 3])
    pvs = get_elements('setpoint', ['x', 'y'],
                       unit_conversion=linear_conversion)
    pvs['x'].put_pv_value('x', 4.0, unit='machine')
    pvs['y'].put_pv_value('y', 4.0, unit='physics')
    value_physics = pvs['x'].get_pv_value('setpoint', 'x', 'physics')
    value_machine = pvs['y'].get_pv_value('setpoint', 'y', 'machine')
    assert value_physics == 11.0
    assert value_machine == 0.5


def test_quadratic_equation():
    pvs = get_elements('setpoint', ['x', 'y'],
                       unit_conversion=UnitConversion([1, 2, 3]))

    pvs['x'].put_pv_value('x', 4.0, unit='machine')
    value_physics = pvs['x'].get_pv_value('setpoint', 'x', 'physics')
    assert value_physics == 27.0

    with pytest.raises(ValueError):
        pvs['y'].put_pv_value('y', 2.5, unit='physics')
