from pml.exceptions import PvException
import pml.element
import pml.device
import cs_dummy
from pml.physics import Physics
from pml.units import UcPoly
import pytest


@pytest.fixture
def get_elements(length=0.0, uc=UcPoly([0, 1])):
    cs = cs_dummy.CsDummy()

    element = pml.element.Element(1, 'Quad', Physics(6))
    rb_pv = 'SR22C-DI-EBPM-04:SA:X'
    sp_pv = 'SR22C-DI-EBPM-04:SA:Y'
    device1 = pml.device.Device(rb_pv, sp_pv, cs)
    device2 = pml.device.Device(sp_pv, rb_pv, cs)

    element.add_device('x', device1, uc)
    element.add_device('y', device2, uc)

    return element


def test_create_element():
    physics = Physics(length=6.0)
    e = pml.element.Element(4, 'Quad', physics)
    e.add_to_family('BPM')
    assert 'BPM' in e.families
    assert e.get_length() == 6.0


def test_add_element_to_family():
    physics = Physics(length=6.0)
    e = pml.element.Element('dummy', 'Quad', physics)
    e.add_to_family('fam')
    assert 'fam' in e.families


def test_readback_pvs():
    # Tests to get/set pv names and/or values
    element = get_elements()
    element.put_pv_value('x', 40.0)
    element.put_pv_value('y', 40.0)
    assert isinstance(element.get_pv_value('x', 'readback',
                                           unit='physics'), float)
    assert isinstance(element.get_pv_value('y', 'readback'), float)
    assert isinstance(element.get_pv_name('x'), list)
    assert isinstance(element.get_pv_name('y', 'readback'), str)


def test_setpoint_pvs():
    element = get_elements()
    element.put_pv_value('x', 40.0)
    element.put_pv_value('y', 40.0)
    assert isinstance(element.get_pv_value('x', 'setpoint'), float)
    assert isinstance(element.get_pv_value('y', 'setpoint'), float)
    assert isinstance(element.get_pv_name('x'), list)
    assert isinstance(element.get_pv_name('y', 'setpoint'), str)


def test_get_pv_exceptions():
    element = get_elements()
    with pytest.raises(PvException):
        element.get_pv_value('setpoint', 'unknown_field')
    with pytest.raises(PvException):
        element.get_pv_value('unknown_handle', 'y')

    with pytest.raises(PvException):
        element.get_pv_name('unknown_handle')


def test_identity_conversion():
    uc_id = UcPoly([1, 0])
    element = get_elements(uc=uc_id)
    element.put_pv_value('x', 4.0, unit='machine')
    value_physics = element.get_pv_value('x', 'setpoint', 'physics')
    element.put_pv_value('x', 4.0, unit='physics')
    value_machine = element.get_pv_value('x', 'setpoint', 'machine')
    assert value_machine == 4.0
    assert value_physics == 4.0

'''
#    dummy_control_system.get = mock.MagicMock(return_value=4)
#    self._cs.get('duumy')
#    dummy_control_system.get.assert_called_with('dummy')
#    dummy_control_system.set.assert_called_with(pv, value)
'''
