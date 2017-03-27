from pml.exceptions import PvException
import pml.element
import pml.device
import cs_dummy
from pml.physics import Physics
from pml.units import UcPoly
import pytest


@pytest.fixture
def get_element(length=0.0, uc=UcPoly([1, 0])):
    cs = cs_dummy.CsDummy()

    element = pml.element.Element(1, 'Quad', Physics(6))
    rb_pv = 'SR22C-DI-EBPM-04:SA:X'
    sp_pv = 'SR22C-DI-EBPM-04:SA:Y'
    device1 = pml.device.Device(cs, rb_pv, sp_pv)
    device2 = pml.device.Device(cs, sp_pv, rb_pv)

    element.add_device('x', device1, uc)
    element.add_device('y', device2, uc)

    return element


def test_create_element():
    physics = Physics(length=6.0)
    e = pml.element.Element('bpm1', 6.0, 'bpm', physics)
    e.add_to_family('BPM')
    assert 'BPM' in e.families
    assert e.get_length() == 6.0


def test_add_element_to_family():
    physics = Physics(length=6.0)
    e = pml.element.Element('dummy', 'Quad', physics)
    e.add_to_family('fam')
    assert 'fam' in e.families


@pytest.mark.parametrize('pv_type', ['readback', 'setpoint'])
def test_readback_pvs(pv_type):
    # Tests to get/set pv names and/or values
    # The default unit conversion is identity
    element = get_element()
    element.put_pv_value('x', 40.0)
    element.put_pv_value('y', 40.0)
    assert element.get_pv_value('x', pv_type, unit='physics') == 40.0
    assert element.get_pv_value('x', pv_type, unit='hardware') == 40.0
    assert element.get_pv_value('y', pv_type, unit='physics') == 40.0
    assert element.get_pv_value('y', pv_type, unit='hardware') == 40.0
    assert isinstance(element.get_pv_name('x'), list)
    assert isinstance(element.get_pv_name('y'), list)
    assert isinstance(element.get_pv_name('x', pv_type), str)
    assert isinstance(element.get_pv_name('y', pv_type), str)


def test_get_pv_exceptions():
    element = get_element()
    with pytest.raises(PvException):
        element.get_pv_value('setpoint', 'unknown_field')
    with pytest.raises(PvException):
        element.get_pv_value('unknown_handle', 'y')

    with pytest.raises(PvException):
        element.get_pv_name('unknown_handle')


def test_identity_conversion():
    uc_id = UcPoly([1, 0])
    element = get_element(uc=uc_id)
    element.put_pv_value('x', 4.0, unit='machine')
    value_physics = element.get_pv_value('x', 'setpoint', 'physics')
    element.put_pv_value('x', 4.0, unit='physics')
    value_machine = element.get_pv_value('x', 'setpoint', 'machine')
    assert value_machine == 4.0
    assert value_physics == 4.0
