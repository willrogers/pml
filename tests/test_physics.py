import rml.physics
import cs_dummy
import pytest


@pytest.fixture
def create_device(readback, setpoint):
    _rb = readback
    _sp = setpoint
    _cs = cs_dummy.CsDummy()
    _uc = None
    device = rml.device.Device(_rb, _sp, _cs, _uc)
    return device


def test_put_pv_value():
    device = create_device('rb_pv', 'sp_pv')
    assert device
