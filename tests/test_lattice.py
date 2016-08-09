import pytest
import rml.lattice
import rml.element


DUMMY_NAME = 'dummy'


@pytest.fixture
def simple_element():
    element_length = 1.5
    e = rml.element.Element('dummy_element', element_length)
    return e


@pytest.fixture
def simple_element_and_lattice(simple_element):
    l = rml.lattice.Lattice(DUMMY_NAME)
    l.append_element(simple_element)
    return simple_element, l


def test_create_lattice():
    l = rml.lattice.Lattice(DUMMY_NAME)
    assert(len(l)) == 0
    assert l.name == DUMMY_NAME


def test_non_negative_lattice():
    l = rml.lattice.Lattice(DUMMY_NAME)
    assert(len(l)) >= 0


def test_lattice_with_one_element(simple_element_and_lattice):
    element, lattice = simple_element_and_lattice
    # There is one element in the lattice.
    assert(len(lattice) == 1)
    # The total length of the lattice is the same as its one element.
    assert lattice.get_length() == element.length
    # Get all elements
    assert lattice.get_elements() == [element]


def test_lattice_get_element_with_family(simple_element_and_lattice):
    element, lattice = simple_element_and_lattice
    element.add_to_family('fam')
    assert lattice.get_elements('fam') == set([element])
    assert lattice.get_elements('nofam') == set()
