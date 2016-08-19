import rml.machines
import rml.load
import pytest

from math import floor


@pytest.mark.xfail
def test_machine_load_elements():
    lattice = rml.machines.get_elements(machine='SRI21', elem_type='BPM')
    assert len(lattice) == 173
    for element in lattice.get_elements():
        assert isinstance(element.get_pv_name('readback', 'x'), str)
        assert isinstance(element.get_pv_name('readback', 'y'), str)


def test_load_lattice():
    lattice = rml.load.load_lattice('/home/cxa78676/rml/tests/data/SRI21/')
    assert len(lattice) == 2428
    assert floor(lattice.get_length()) == 561.0
