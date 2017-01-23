import pytest
import pml.lattice
import pml.element
import pml.device
import cs_dummy
import mock
from pml.units import UcPoly

DUMMY_NAME = 'dummy'


@pytest.fixture
def simple_element(identity=1):
    cs = cs_dummy.CsDummy()
    uc = UcPoly([0, 1])

    # Create devices and attach them to the element
    element = pml.element.Element(identity, 'BPM', mock.MagicMock())
    rb_pv = 'SR22C-DI-EBPM-04:SA:X'
    sp_pv = 'SR22C-DI-EBPM-04:SA:Y'
    device1 = pml.device.Device(rb_pv, sp_pv, cs)
    device2 = pml.device.Device(sp_pv, rb_pv, cs)
    element.add_to_family('BPM')

    element.add_device('x', device1, uc)
    element.add_device('y', device2, uc)

    return element


@pytest.fixture
def simple_element_and_lattice(simple_element):
    l = pml.lattice.Lattice(DUMMY_NAME)
    l.add_element(simple_element)
    return simple_element, l


def test_create_lattice():
    l = pml.lattice.Lattice('DUMMY_NAME')
    assert(len(l)) == 0
    assert l.name == 'DUMMY_NAME'


def test_non_negative_lattice():
    l = pml.lattice.Lattice(DUMMY_NAME)
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


def test_get_family_value(simple_element_and_lattice):
    element, lattice = simple_element_and_lattice
    lattice.set_family_value('BPM', 'x', [2.3])
    family_values = lattice.get_family_value('BPM', 'x')
    assert family_values == list([2.3])
