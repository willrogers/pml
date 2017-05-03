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
        '''
        Get the keys of the devices dictionary.
        '''
        return self._devices.keys()

    def get_length(self):
        '''
        Get the length of an element.
        '''

        return self._length

    def __repr__(self):
        '''
        Get all families the element is part of.
        '''
        return str(self.families)

    def is_enabled(self):
        '''
        Check whether an element is enabled.
        '''
        return self._enabled

    def set_enabled(self, enabled=True):
        '''
        Enable or disable an element.
        '''
        self._enabled = enabled

    def add_device(self, field, device, uc):
        '''
        Add device and a unit conversion objects to a given field.
        '''
        self._devices[field] = device
        self._uc[field] = uc

    def get_device(self, field):
        '''
        For a given field get the device of an element.
        '''
        return self._devices[field]

    def add_to_family(self, family):
        '''
        Add a family to an element.
        '''
        self.families.add(family)

    def get_pv_value(self, field, handle, unit=pml.ENG, sim=False):
        '''
        Get the pv value of an element given a field and a handle.
        This value can be either real or from the simulation.
        Unit type is optional.
        '''
        if not sim:
            if field in self._devices:
                value = self._devices[field].get_value(handle)
                if unit == pml.PHY:
                    value = self._uc[field].machine_to_physics(value)
                return value
            else:
                raise PvException("No device associated with field {0}")
        else:
            value = self._physics.get_value(field, handle, unit)
            if unit == pml.ENG:
                value = self._uc[field].machine_to_physics(value)
            return value

    def put_pv_value(self, field, value, unit=pml.ENG, sim=False):
        '''
        Set the pv value for a PV. This value can be either on the machine
        or in the simulation. A field is required to identify a device.
        Unit type is optional.
        '''
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
        '''
        Get the pv name of an element given a field and a handle.
        '''
        try:
            return self._devices[field].get_pv_name(handle)
        except KeyError:
            raise PvException('Element has no device for field {}'.format(field))
