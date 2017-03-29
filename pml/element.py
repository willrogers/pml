from pml.exceptions import PvException


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

    def get_length(self):
        return self._length

    def __repr__(self):
        return str(self.families)

    def add_device(self, field, device, uc):
        self._devices[field] = device
        self._uc[field] = uc

    def get_device(self, field):
        return self._devices[field]

    def add_to_family(self, family):
        self.families.add(family)

    def get_pv_value(self, field, handle, unit='machine', sim=False):
        if not sim:
            if field in self._devices:
                value = self._devices[field].get_value(handle)
                if unit == 'physics':
                    value = self._uc[field].machine_to_physics(value)
                return value
            else:
                raise PvException("No device associated with field {0}")
        else:
            value = self._physics.get_value(field, handle, unit)
            if unit == 'machine':
                value = self._uc[field].machine_to_physics(value)
            return value

    def put_pv_value(self, field, value, unit='machine', sim=False):
        if not sim:
            if field in self._devices:
                if unit == 'physics':
                    value = self._uc[field].physics_to_machine(value)
                self._devices[field].put_value(value)
            else:
                raise PvException('''There is no device associated with
                                     field {0}'''.format(field))
        else:
            if unit == 'machine':
                value = self._uc[field].machine_to_physics(value)
            self._physics.put_value(field, value)

    def get_pv_name(self, field, handle='*', sim=False):
        if not sim:
            if field in self._devices:
                return self._devices[field].get_pv_name(handle)
        else:
            return self._physics.get_pv_name(field, handle)
        raise PvException("There is no device associated with field {0}"
                          .format(field))
