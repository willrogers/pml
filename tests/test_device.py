from rml.exceptions import PvException
import rml.device
import cs_dummy
import pytest


rb = 'SR01A-PC-SQUAD-01:I'
sp = 'SR01A-PC-SQUAD-01:SETI'


@pytest.fixture
def create_device(readback, setpoint):
    _rb = readback
    _sp = setpoint
    _cs = cs_dummy.DummyControlSystem()
    _uc = None
    device = rml.device.Device(_rb, _sp, _cs, _uc)
    return device


def test_set_device_value():
    device1 = create_device(rb, sp)
    device1.put_value(40, 'machine')
    assert device1.get_value('setpoint', 'machine') == 40

    device2 = create_device(rb, None)
    with pytest.raises(PvException):
        device2.put_value(40, 'machine')
