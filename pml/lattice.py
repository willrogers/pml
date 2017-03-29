class Lattice(object):

    def __init__(self, name):
        self.name = name
        self._lattice = []

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
        family_values = list()
        for element in self._lattice:
            if family in element.families:
                if handle == 'setpoint':
                    family_values.append(element.get_pv_value(
                        field, 'setpoint'))
                elif handle == 'readback':
                    family_values.append(element.get_pv_value(
                        field, 'readback'))

        return family_values

    def set_family_value(self, family, field, values):
        # Get the number of elements in the family
        elements_in_family = 0
        family_elements = list()

        # Find out how many elements are in the given family
        for element in self._lattice:
            if family in element.families:
                elements_in_family += 1
                family_elements.append(element)

        # if number of given elements is not equal to the size of
        # the given array, raise an exception
        if elements_in_family != len(values):
            raise Exception("""Number of elements in given array must be equal
            to the number of elements in the lattice""")

        # change the value of each element in the computed list to the
        # one in the given value array
        for element, value in zip(family_elements, values):
            element.put_pv_value(field, value)
