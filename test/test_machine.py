import pml.load
import pytest
import os
import re
import mock

from math import floor


@pytest.fixture
def lattice():
    basepath = os.path.dirname(__file__)
    filename = os.path.join(basepath, 'data/SRI21/')
    lattice = pml.load.load_lattice(filename, mock.MagicMock())
    return lattice


def test_load_bpms(lattice):
    bpms = lattice.get_elements('BPM')
    for bpm in bpms:
        assert set(bpm.devices.keys()) == set(('x', 'y'))
    assert len(bpms) == 173


def test_load_drift_elements(lattice):
    drifts = lattice.get_elements('DRIFT')
    assert len(drifts) == 1268


def test_load_quadrupoles(lattice):
    quads = lattice.get_elements('QUAD')
    assert len(quads) == 248
    for quad in quads:
        assert set(quad.devices.keys()) == set(('b1',))
        device = quad.devices['b1']
        assert re.match('SR.*Q.*:I', device.rb_pv)
        assert re.match('SR.*Q.*:SETI', device.sp_pv)
        quad.put_pv_value('b1', 1)
        device.cs.put.assert_called_with(device.sp_pv, 1)


def test_load_quad_family(lattice):
    q1b = lattice.get_elements('Q1B')
    assert len(q1b) == 36
    q1b = lattice.get_elements('Q1D')
    assert len(q1b) == 12


def test_load_correctors(lattice):
    hcm = lattice.get_elements('HSTR')
    vcm = lattice.get_elements('VSTR')
    assert len(hcm) == 172
    assert len(vcm) == 172


def test_load_lattice(lattice):
    assert len(lattice) == 2428
    assert floor(lattice.get_length()) == 561.0
