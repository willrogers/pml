import rml.load
import pytest
import os

from math import floor


@pytest.fixture
def init():
    basepath = os.path.dirname(__file__)
    filename = os.path.join(basepath, 'data/SRI21/')
    lattice = rml.load.load_lattice(filename)
    return lattice


@pytest.mark.xfail
def test_load_bpms():
    lattice = init()
    assert len(lattice) == 173
    for element in lattice.get_elements():
        assert isinstance(element.get_pv_name('readback', 'x'), str)
        assert isinstance(element.get_pv_name('readback', 'y'), str)


def test_load_drift():
    lattice = init()
    drifts = lattice.get_elements('DRIFT')
#    for drift in drifts:
#        assert drift.get_pv_name('x') == None


def test_load_lattice():
    lattice = init()
    assert len(lattice) == 2428
    assert floor(lattice.get_length()) == 561.0
