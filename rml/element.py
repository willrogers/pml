''' Representation of an element
@param element_type: type of the element
@param length: length of the element
'''
from rml.exceptions import PvException
from rml.units import UcPoly


class Element(object):

    def __init__(self, elem_identity, **kwargs):
        '''
        Possible arguments for kwargs:

        :str elem_identity: identifier used to match an element to a pv
        :set elem_family: a set used to store families
        :param cs: type of control system to be used
        '''
        self.identity = elem_identity
        self.families = set()
        self.length = kwargs.get('length', 0)
        self._cs = kwargs.get('cs', None)
        unit_conversion = UcPoly([1, 0])
        self._uc = kwargs.get('uc', unit_conversion)
        self.devices = dict()

    def add_device(self, field, device):
        self.devices[field] = device

    def add_to_family(self, family):
        self.families.add(family)

    def get_pv_value(self, field, handle, unit='machine'):
        if field in self.devices:
            return self.devices[field].get_value(handle, unit)
        else:
            raise PvException("There is no device associated with field {0}"
                              .format(field))

    def put_pv_value(self, field, value, unit='machine'):
        if field in self.devices:
            self.devices[field].put_value(value, unit)
        else:
            raise PvException("There is no device associated with field {0}"
                              .format(field))

    def get_pv_name(self, field, handle='*'):
        if field in self.devices:
            return self.devices[field].get_pv_name(handle)
        else:
            raise PvException("There is no device associated with field {0}"
                              .format(field))
