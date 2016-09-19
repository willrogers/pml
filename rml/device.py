from rml.exceptions import PvException
from rml.cs_dummy import CsDummy
from rml.exceptions import PvException


class Device(object):
    # should be a length parameter here
    def __init__(self, length, rb_pv=None, sp_pv=None, cs=CsDummy(), uc=None):
        self.length = length
        self.rb_pv = rb_pv
        self.sp_pv = sp_pv
        assert not (rb_pv is None and sp_pv is None)
        if rb_pv is not None:
            self.name = rb_pv.split(':')[0]
        elif sp_pv is not None:
            self.name = sp_pv.split(':')[0]
        else:
            raise PvException("Readback or setpoint pvs need to be given")

    def put_value(self, value):
        # Not sure if this method will need a handle flag to set
        # an initial value for readback pvs. Suppose not:
        if self.sp_pv is not None:
            self.cs.put(self.sp_pv, value)
        else:
            raise PvException("""This device {0} has no setpoint pv."""
                              .format(self.name))

    def get_value(self, handle, unit):
        if handle == 'readback' and self.rb_pv:
            if unit == 'machine':
                return self.cs.get(self.rb_pv)
            elif unit == 'physics':
                machine_value = self.cs.get(self.rb_pv)
                return self.uc.machine_to_physics(machine_value)
        elif handle == 'setpoint' and self.sp_pv:
            if unit == 'machine':
                return self.cs.get(self.sp_pv)
            elif unit == 'physics':
                machine_value = self.cs.get(self.sp_pv)
                return self.uc.machine_to_physics(machine_value)

        raise PvException("""This device {0} has no {1} pv."""
                          .format(self.name, handle))

    def get_pv_name(self, handle):
        if handle == '*':
            return [self.rb_pv, self.sp_pv]
        elif handle == 'readback':
            return self.rb_pv
        elif handle == 'setpoint':
            return self.sp_pv
