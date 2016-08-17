class Lattice(object):

    def __init__(self, name):
        self.name = name
        self._elements = []

    def __len__(self):
        ''' Get the number of elements in the lattice '''
        return len(self._elements)

    def get_length(self):
        ''' Get the length of the lattice in meters '''
        total_length = 0
        for e in self._elements:
            total_length += e.length
        return total_length

    def add_element(self, element):
        '''
        Add an element to the lattice
        # TODO: modify method to accept a set() arg
        '''
        self._elements.append(element)

    def get_elements(self, family='*'):
        '''
        Get all elements of a lattice from a specified family.
        If no family is specified, return all elements
        '''
        if family == '*':
            return self._elements

        matched_elements = set()
        for element in self._elements:
            if family in element.families:
                matched_elements.add(element)
        return matched_elements

    def get_name(self):
        ''' Get the name of the lattice '''
        return self.name
