''' Representation of an element
@param element_type: type of the element
@param length: length of the element
'''
from rml.exceptions import PvUnknownFieldError, PvUnknownHandleError


class Element(object):

    def __init__(self, elem_identity, elem_family, **kwargs):
        '''
        Possible arguments for kwargs:

        :str elem_identity: identifier used to match an element to a pv
        :set elem_family: a set used to store families
        :param cs: type of control system to be used
        '''
        self.identity = elem_identity
        self.families = set()
        self.families.add(elem_family)
        self.length = kwargs.get('length', 0)
        self._cs = kwargs.get('cs', None)
        # Keys represent fields and values pv names.
        self.pv = dict()

    def add_to_family(self, family):
        self.families.add(family)

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

    def put_pv_name(self, field, pv_name):
        self.pv[field] = pv_name

'''
    def get_pv_name(self, field):
            Can be changed to accept one pv
        return self.pv[field]

'''
