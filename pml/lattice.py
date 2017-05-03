from pml.exceptions import PvException
from pml.exceptions import ElementNotFoundException

class Lattice(object):
    ''' Simple lattice object to hold the elements of the ring. '''

    def __init__(self, name, control_system):
        self.name = name
        self._lattice = []
        self._cs = control_system

    def __getitem__(self, n):
        '''
        Get the nth element element of the lattice.
        '''
        return self._lattice[n]

    def __len__(self):
        '''
        Get the number of elements in the lattice.
        '''
        return len(self._lattice)

    def get_length(self):
        '''
        Get the length of the lattice in meters.
        '''
        total_length = 0
        for e in self._lattice:
            total_length += e.get_length()
        return total_length

    def add_element(self, element):
        '''
        Add an element to the lattice.
        '''
        self._lattice.append(element)

    def get_elements(self, family=None):
        '''
        Get all elements of a lattice from a specified family.
        If no family is specified, return all elements.
        '''
        if family is None:
            return self._lattice

        matched_lattice = list()
        for element in self._lattice:
            if family in element.families:
                matched_lattice.append(element)
        return matched_lattice

    def get_all_families(self):
        '''
        Get all available families inside the lattice.
        '''
        families = set()
        for element in self._lattice:
            for family in element.families:
                families.add(family)

        return families

    def get_family_pvs(self, family, field, handle):
        '''
        Get all pvs from a specified family, field and handle.
        '''
        elements = self.get_elements(family)
        pv_names = []
        for element in elements:
            pv_names.append(element.get_pv_name(field, handle))
        return pv_names

    def get_family_values(self, family, field, handle='setpoint'):
        '''
        Get all pv values from a specified family, field and handle.
        '''
        pv_names = self.get_family_pvs(family, field, handle)
        return self._cs.get(pv_names)

    def set_family_values(self, family, field, values):
        '''
        Given a family set the values of the pvs from a specified field.
        '''
        # Get the number of elements in the family
        pv_names = self.get_family_pvs(family, field, 'setpoint')
        if len(pv_names) != len(values):
            raise PvException("""Number of elements in given array must be equal
                                 to the number of elements in the lattice""")
        self._cs.put(pv_names, values)

    def get_s(self, given_element):
        '''
        Return the position of a given element in the lattice.
        '''
        s_pos = 0
        for element in self._lattice:
            if element is not given_element:
                s_pos += element.get_length()
            else:
                return s_pos
        raise ElementNotFoundException('Given element does not exist in the lattice')

    def get_family_s(self, family):
        '''
        Return a list of positions for a given family.
        '''
        elements = self.get_elements(family)
        s_positions = list()
        for element in elements:
            s_positions.append(self.get_s(element))
        return s_positions
