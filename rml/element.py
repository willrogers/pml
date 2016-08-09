''' Representation of an element
@param element_type: type of the element
@param length: length of the element
'''
class Element:
    def __init__(self, elem_type, length):
        # TODO: use **kwargs
        self.element_type = elem_type
        self.length = length
        self.families = []

############################## Utility methods ###############################

    def add_to_family(self, family):
        self.families.append(family)

############################## Accessor methods ##############################

    def get_type(self):
        return self.element_type


    def get_length(self):
        return self.length


    def get_families(self):
        return self.families
