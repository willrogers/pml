''' Representation of an element
@param element_type: type of the element
@param length: length of the element
'''
import pkg_resources
pkg_resources.require('cothread')
from cothread.catools import caget

class Element(object):

    def __init__(self, element_type, length, **kwargs):
        self.element_type = element_type
        self.length = length
        self.families = set()

        # Getting the pv value
        self.pv = kwargs.get('pv', None)
        self._field = {'x', 'y'}

    def add_to_family(self, family):
        self.families.add(family)

    def get_pv(self, field, handle='readback'):
        """
        Get pv value for the given field.
        Currently only supports readback handle
        """

        if not field in self._field:
            raise RuntimeError("Field {0} doesn't exist.".format(field))
        elif handle == 'readback':
            return caget(self.pv)
        else:
            raise ValueError("Unknown handle {0}".format(handle))

    def get_type(self):
        return self.element_type

    def get_length(self):
        return self.length

    def get_families(self):
        return self.families
