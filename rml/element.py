# TODO: make element as an abstract class
class Element:
    # TODO: use **kwargs
    def __init__(self, name, length):
        self.element_type = name
        self.length = length
        self.families = []


    def add_to_family(self, family):
        self.families.append(family)
