class Lattice(object):

    def __init__(self, name):
        self.name = name
        self._elements = []

    def __len__(self):
        ''' The number of elements in the lattice '''
        return len(self._elements)

    def append_element(self, element):
        # TODO: modify method to accept a set() arg
        self._elements.append(element)

    def get_length(self):
        ''' Length of the lattice '''
        total_length = 0
        for e in self._elements:
            total_length += e.length
        return total_length

    def get_elements(self, family='*'):
        ''' Get all elements of a lattice from a specified family '''
        if family == '*':
            return self._elements

        matched_elements = set()
        for element in self._elements:
            if family in element.get_families():
                matched_elements.add(element)
        return matched_elements

    def get_name(self):
        return self.name
