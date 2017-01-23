from pml.exceptions import PvException
import pml.device
import cs_dummy
import pytest


@pytest.fixture
def create_device(readback, setpoint):
    _rb = readback
    _sp = setpoint
    _cs = cs_dummy.CsDummy()
    _uc = None
    device = pml.device.Device(rb_pv=_rb, sp_pv=_sp, cs=_cs)
    return device


def test_set_device_value():
    rb_pv = 'SR01A-PC-SQUAD-01:I'
    sp_pv = 'SR01A-PC-SQUAD-01:SETI'

    device1 = create_device(rb_pv, sp_pv)

    device1.put_value(40)
    assert device1.get_value('setpoint') == 40

    device2 = create_device(rb_pv, None)
    with pytest.raises(PvException):
        device2.put_value(40)
