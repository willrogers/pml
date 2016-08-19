import rml.load
import pytest

from math import floor


@pytest.fixture
def init():
    lattice = rml.load.load_lattice('/home/cxa78676/rml/tests/data/SRI21/')
    return lattice


def test_load_bpms():
    lattice = init()
    assert len(lattice) == 173
    for element in lattice.get_elements():
        assert isinstance(element.get_pv_name('readback', 'x'), str)
        assert isinstance(element.get_pv_name('readback', 'y'), str)


def test_load_drift():
    lattice = init()
    drifts = lattice.get_elements('DRIFT')
    for drift in drifts:
        assert drift.get_pv_name('x') == None


def test_load_lattice():
    lattice = init()
    assert len(lattice) == 2428
    assert floor(lattice.get_length()) == 561.0
