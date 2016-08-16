''' Representation of an element
@param element_type: type of the element
@param length: length of the element
'''
from rml.exceptions import PvUnknownFieldError, PvUnknownHandleError


class Element(object):

    def __init__(self, element_name, element_type, length=0, **kwargs):
        '''
        Possible arguments for kwargs:

        :param cs: type of control system to be used
        '''
        self.element_type = element_type
        self.name = element_name
        self.length = length
        self.families = set()
        self._cs = kwargs.get('cs', None)
        # To store the pv. Keys represent fields and values pv names.
        self.pv = dict()

    def get_type(self):
        return self.element_type

    def get_length(self):
        return self.length

    def get_families(self):
        return self.families

    def add_to_family(self, family):
        self.families.add(family)

    def get_pv_name(self, field):
        return self.pv[field]

    def put_pv_name(self, field, pv_name):
        self.pv[field] = pv_name

    def get_pv_value(self, field, handle='readback'):
        """
        Get pv value for the given field.
        Currently, only supports readback handle
        """

        if field not in self.pv:
            raise PvUnknownFieldError("Unknown field {0}.".format(field))
        elif handle == 'readback':
            return self._cs.get(self.pv[field])
        else:
            raise PvUnknownHandleError("Unknown handle {0}".format(handle))

    def put_pv_value(self, field, value):
        ''' Set the pv value. No need for handle because only the setback value
        can be set'''
        if field not in self.pv:
            raise PvUnknownFieldError("Unknown field {0}.".format(field))
        else:
            self._cs.put(self.pv[field], value)
