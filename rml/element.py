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
        self.readback = dict()
        self.setpoint = dict()

    def add_to_family(self, family):
        self.families.add(family)

    def get_pv_value(self, handle, field):
        """
        Get pv value for the given field.
        Currently, only supports readback handle
        """

        if handle == 'readback':
            if field not in self.readback:
                raise PvUnknownFieldError("Unknown field {0}.".format(field))
            else:
                return self._cs.get(self.readback[field])
        elif handle == 'setpoint':
            if field not in self.setpoint:
                raise PvUnknownFieldError("Unknown field {0}.".format(field))
            else:
                return self._cs.get(self.setpoint[field])
        else:
            raise PvUnknownHandleError("Unknown handle {0}.".format(field))

    def put_pv_value(self, field, value):
        ''' Set the pv value. No need for handle because only the setback value
        can be set'''
        if field not in self.setpoint:
            raise PvUnknownFieldError("Unknown field {0}.".format(field))
        else:
            self._cs.put(self.setpoint[field], value)

    def put_pv_name(self, handle, field, pv_name):
        if handle == 'setpoint' or handle == 'put':
            self.setpoint[field] = pv_name
        elif handle == 'readback' or handle == 'get':
            self.readback[field] = pv_name
        else:
            raise PvUnknownHandleError("Unknown handle {0}".format(handle))

    def get_pv_name(self, handle, field='*'):
        if handle == 'setpoint':
            if field == '*':
                return self.setpoint
            else:
                return self.setpoint[field]
        elif handle == 'readback':
            if field == '*':
                return self.readback
            else:
                return self.readback[field]
        else:
            raise PvUnknownHandleError("Unknown handle {0}".format(field))
