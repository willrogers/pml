from pml.exceptions import PvException
from pml.exceptions import ElementNotFoundException


class Lattice(object):

    def __init__(self, name, control_system):
        self.name = name
        self._lattice = []
        self._cs = control_system

    def __getitem__(self, i):
        return self._lattice[i]

    def __len__(self):
        ''' Get the number of elements in the lattice '''
        return len(self._lattice)

    def __str__(self):
        print(self._lattice)

    def get_length(self):
        ''' Get the length of the lattice in meters '''
        total_length = 0
        for e in self._lattice:
            total_length += e.get_length()
        return total_length

    def add_element(self, element):
        '''
        Add an element to the lattice
        # TODO: modify method to accept a set() arg
        '''
        self._lattice.append(element)

    def get_elements(self, family='*'):
        '''
        Get all elements of a lattice from a specified family.
        If no family is specified, return all elements
        '''
        if family == '*':
            return self._lattice

        matched_lattice = list()
        for element in self._lattice:
            if family in element.families:
                matched_lattice.append(element)
        return matched_lattice

    def get_all_families(self):
        families = set()
        for element in self._lattice:
            for family in element.families:
                families.add(family)

        return families

    def get_pv_names(self, family, field, handle):
        elements = self.get_elements(family)
        pv_names = []
        for element in elements:
            pv_names.append(element.get_pv_name(field, handle))
        return pv_names

    def get_family_value(self, family, field, handle='setpoint'):
        pv_names = self.get_pv_names(family, field, handle)
        return self._cs.get(pv_names)

    def set_family_value(self, family, field, values):
        # Get the number of elements in the family
        pv_names = self.get_pv_names(family, field, 'setpoint')
        if len(pv_names) != len(values):
            raise PvException("""Number of elements in given array must be equal
            to the number of elements in the lattice""")
        self._cs.put(pv_names, values)

    def get_s(self, given_element):
        s_pos = 0
        for element in self._lattice:
            if element is not given_element:
                s_pos += element.get_length()
            else:
                return s_pos
        raise ElementNotFoundException('Given element does not exist in the lattice')
