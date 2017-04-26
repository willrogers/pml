from pml.exceptions import PvException
import pml.element
import pml.device
from pml.physics import Physics
from pml.units import UcPoly
import pytest
import mock


@pytest.fixture
def get_element(length=0.0, uc=UcPoly([1, 0])):

    mock_cs = mock.MagicMock()
    mock_cs.get.return_value = 40.0

    element = pml.element.Element(1, 'Quad', Physics(6))
    rb_pv = 'SR22C-DI-EBPM-04:SA:X'
    sp_pv = 'SR22C-DI-EBPM-04:SA:Y'
    device1 = pml.device.Device(mock_cs, rb_pv, sp_pv)
    device2 = pml.device.Device(mock_cs, sp_pv, rb_pv)

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
    value_physics = element.get_pv_value('x', 'setpoint', 'physics')
    value_machine = element.get_pv_value('x', 'setpoint', 'machine')
    assert value_machine == 40.0
    assert value_physics == 40.0


def test_get_fields(get_element):
    element = get_element
    assert set(element.get_fields()) == set(['y', 'x'])
