import pytest
import rml.lattice
import rml.element
import mock

DUMMY_NAME = 'dummy'


@pytest.fixture
def simple_element():
    e_length = 1.5
    e = rml.element.Element('dummy_element', 'Quad', mock.MagicMock())
    return e


@pytest.fixture
def simple_element_and_lattice(simple_element):
    l = rml.lattice.Lattice(DUMMY_NAME)
    l.add_element(simple_element)
    return simple_element, l


def test_create_lattice():
    l = rml.lattice.Lattice('DUMMY_NAME')
    assert(len(l)) == 0
    assert l.name == 'DUMMY_NAME'


def test_non_negative_lattice():
    l = rml.lattice.Lattice(DUMMY_NAME)
    assert(len(l)) >= 0


def test_lattice_with_n_elements(simple_element_and_lattice):
    elem, lattice = simple_element_and_lattice

    # Getting elements
    lattice.add_element(elem)
    assert lattice[0] == elem
    assert lattice.get_elements() == [elem, elem]


def test_lattice_get_element_with_family(simple_element_and_lattice):
    element, lattice = simple_element_and_lattice
    element.add_to_family('fam')
    assert lattice.get_elements('fam') == [element]
    assert lattice.get_elements('nofam') == []


def test_get_all_families(simple_element_and_lattice):
    element, lattice = simple_element_and_lattice
    families = lattice.get_all_families()
    assert len(families) > 0
