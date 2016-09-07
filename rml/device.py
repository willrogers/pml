from rml.exceptions import PvException


class Device(object):
    def __init__(self, rb_pv=None, sp_pv=None, cs=None, uc=None):
        self.rb_pv = rb_pv
        self.sp_pv = sp_pv
        self._cs = cs
        self._uc = uc
        assert not (rb_pv is None and sp_pv is None)
        if rb_pv:
            self.name = rb_pv.split(':')[0]
        else:
            self.name = sp_pv.split(':')[0]

    def put_value(self, value, unit):
        # Not sure if this method will need a handle flag to set
        # an initial value for readback pvs. Suppose not:
        if self.sp_pv:
            if unit == 'machine':
                self._cs.put(self.sp_pv, value)
            elif unit == 'physics':
                machine_value = self._uc.physics_to_machine(value)
                self._cs.put(self.sp_pv, machine_value)
        else:
            raise PvException("""This device {0} has no setpoint pv."""
                              .format(self.name))

    def get_value(self, handle, unit):
        if handle == 'readback' and self.rb_pv:
            if unit == 'machine':
                return self._cs.get(self.rb_pv)
            elif unit == 'physics':
                machine_value = self._cs.get(self.rb_pv)
                return self._uc.machine_to_physics(machine_value)
        elif handle == 'setpoint' and self.sp_pv:
            if unit == 'machine':
                return self._cs.get(self.sp_pv)
            elif unit == 'physics':
                machine_value = self._cs.get(self.sp_pv)
                return self._uc.machine_to_physics(machine_value)

        raise PvException("""This device {0} has no {1} pv."""
                          .format(self.name, handle))

    def get_pv_name(self, handle):
        if handle == '*':
            return [self.rb_pv, self.sp_pv]
        elif handle == 'readback':
            return self.rb_pv
        elif handle == 'setpoint':
            return self.sp_pv
