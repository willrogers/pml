class Lattice:
    def __init__(self, name):
        self.name = name
        self._elements = []


    def __len__(self):
        ''' The number of elements in the lattice '''
        return len(self._elements)


    # TODO: could modify this to accept a
    # list(.extend) or element arg
    def append_element(self, element):
        self._elements.append(element)


    def length(self):
        ''' Length of the lattice '''
        total_length = 0
        for e in self._elements:
            total_length += e.length
        return total_length


    # TODO return elements for a specific family name
    def get_elements(self, family='*'):
        ''' Get all the elements of a lattice '''
        return self._elements
