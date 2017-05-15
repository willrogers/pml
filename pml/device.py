from pml.exceptions import PvException
import pml


class Device(object):
    # should be a length parameter here
    def __init__(self, cs, rb_pv=None, sp_pv=None):
        self.rb_pv = rb_pv
        self.sp_pv = sp_pv
        self._cs = cs
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
            self._cs.put(self.sp_pv, value)
        else:
            raise PvException("""This device {0} has no setpoint pv."""
                              .format(self.name))

    def get_value(self, handle):
        if handle == pml.RB and self.rb_pv:
            return self._cs.get(self.rb_pv)
        elif handle == pml.SP and self.sp_pv:
            return self._cs.get(self.sp_pv)

        raise PvException("""This device {0} has no {1} pv."""
                          .format(self.name, handle))

    def get_pv_name(self, handle):
        if handle == '*':
            return [self.rb_pv, self.sp_pv]
        elif handle == pml.RB:
            return self.rb_pv
        elif handle == pml.SP:
            return self.sp_pv
