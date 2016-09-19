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


def test_load_bpms():
    lattice = init()
    bpms = lattice.get_elements('BPM')
    assert 'x' in bpms[0].devices.keys()


@pytest.fixture
def test_load_drift_elements():
    # Length of the drifts array is too big
    lattice = init()
    drifts = lattice.get_elements('DRIFT')
    assert len(drifts) == 1268


def test_load_lattice():
    lattice = init()
    assert len(lattice) == 2428
    bpms = lattice.get_elements('BPM')
    drifts = lattice.get_elements('DRIFT')
    assert floor(lattice.get_length()) == 561.0
