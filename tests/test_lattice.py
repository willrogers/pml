import rml.lattice
import rml.element


DUMMY_NAME = 'dummy'


def test_create_lattice():
    l = rml.lattice.Lattice(DUMMY_NAME)
    assert(len(l)) == 0
    assert l.name == DUMMY_NAME


def test_non_negative_lattice():
    l = rml.lattice.Lattice(DUMMY_NAME)
    assert(len(l)) >= 0


def test_lattice_with_one_element():
    l = rml.lattice.Lattice(DUMMY_NAME)
    element_length = 1.5
    e = rml.element.Element('dummy_element', element_length)
    l.append_element(e)
    # There is one element in the lattice.
    assert(len(l) == 1)
    # The total length of the lattice is the same as its one element.
    assert l.length() == element_length
    # Get all elements
    assert l.get_elements() == [e]

