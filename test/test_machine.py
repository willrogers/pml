import pml
import pytest
import os
import re


EPS = 1e-8


@pytest.fixture
def lattice():
    basepath = os.path.dirname(__file__)
    filename = os.path.join(basepath, 'data/VMX/')
    lattice = pml.load_csv.load(filename)
    return lattice


def test_load_lattice(lattice):
    assert len(lattice) == 2476
    assert (lattice.get_length() - 561.571) < EPS


def test_get_pv_names(lattice):
    bpm_x_pvs = lattice.get_pv_names('BPM', 'x', handle='readback')
    assert len(bpm_x_pvs) == 173
    for pv in bpm_x_pvs:
        assert re.match('SR.*BPM.*X', pv)


def test_load_bpms(lattice):
    bpms = lattice.get_elements('BPM')
    for bpm in bpms:
        assert set(bpm._devices.keys()) == set(('x', 'y'))
    assert len(bpms) == 173


def test_load_drift_elements(lattice):
    drifts = lattice.get_elements('DRIFT')
    assert len(drifts) == 1308


def test_load_quadrupoles(lattice):
    quads = lattice.get_elements('QUAD')
    assert len(quads) == 248
    for quad in quads:
        assert set(quad._devices.keys()) == set(('b1',))
        device = quad.get_device('b1')
        assert re.match('SR.*Q.*:I', device.rb_pv)
        assert re.match('SR.*Q.*:SETI', device.sp_pv)


def test_load_quad_family(lattice):
    q1b = lattice.get_elements('Q1B')
    assert len(q1b) == 34
    q1b = lattice.get_elements('Q1D')
    assert len(q1b) == 12


def test_load_correctors(lattice):
    hcm = lattice.get_elements('HSTR')
    vcm = lattice.get_elements('VSTR')
    assert len(hcm) == 173
    assert len(vcm) == 173
