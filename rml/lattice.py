class Lattice:
    def __init__(self, name):
        self.name = name
        self._elements = []


    def __len__(self):
        ''' The number of elements in the lattice '''
        return len(self._elements)

############################## Utility methods ###############################

    def append_element(self, element):
        # TODO: could modify this to accept a
        # list(.extend) or element arg
        self._elements.append(element)


    def get_length(self):
        ''' Length of the lattice '''
        total_length = 0
        for e in self._elements:
            total_length += e.length
        return total_length


    def get_elements(self, family='*'):
        # TODO return elements for a specific family name
        ''' Get all the elements of a lattice from a specified family '''
        return self._elements


############################## Accessor methods ##############################

    def get_name(self):
        return self.name
