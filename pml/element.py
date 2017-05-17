from pml.exceptions import PvException
import pml


class Element(object):

    def __init__(self, name, length, element_type, physics=None):
        '''
        Representation of an element

        Arguments:
            name: unique name of the element
            element_type: element type
            length: length of the element
            physics: physics object
        '''
        self._name = name
        self._type = element_type
        self._length = length
        self._physics = physics
        self.families = set()
        self._uc = dict()
        self._devices = dict()
        self._enabled = True

    def get_fields(self):
        return self._devices.keys()

    def get_length(self):
        return self._length

    def __repr__(self):
        return str(self.families)

    def is_enabled(self):
        return self._enabled

    def set_enabled(self, enabled=True):
        self._enabled = enabled

    def add_device(self, field, device, uc):
        self._devices[field] = device
        self._uc[field] = uc

    def get_device(self, field):
        return self._devices[field]

    def add_to_family(self, family):
        self.families.add(family)

    def get_pv_value(self, field, handle, unit=pml.ENG, sim=False):
        if not sim:
            if field in self._devices:
                value = self._devices[field].get_value(handle)
                if unit == pml.PHY:
                    value = self._uc[field].machine_to_physics(value)
                return value
            else:
                raise PvException("No device associated with field {0}".format(field))
        else:
            value = self._physics.get_value(field, handle, unit)
            if unit == pml.ENG:
                value = self._uc[field].machine_to_physics(value)
            return value

    def put_pv_value(self, field, value, unit=pml.ENG, sim=False):
        if not sim:
            if field in self._devices:
                if unit == pml.PHY:
                    value = self._uc[field].physics_to_machine(value)
                self._devices[field].put_value(value)
            else:
                raise PvException('''There is no device associated with
                                     field {0}'''.format(field))
        else:
            if unit == pml.ENG:
                value = self._uc[field].machine_to_physics(value)
            self._physics.put_value(field, value)

    def get_pv_name(self, field, handle='*'):
        try:
            return self._devices[field].get_pv_name(handle)
        except KeyError:
            raise PvException('Element has no device for field {}'.format(field))

    def get_cs(self, field):
        return self._devices[field].get_cs()
