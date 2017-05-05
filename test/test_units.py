import pytest
from pml.units import UcPoly, UcPchip
import numpy as np


def test_identity_conversion():
    id_conversion = UcPoly([1, 0])
    physics_value = id_conversion.machine_to_physics(4)
    machine_value = id_conversion.physics_to_machine(4)
    assert machine_value == 4
    assert physics_value == 4


def test_linear_conversion():
    linear_conversion = UcPoly([2, 3])
    physics_value = linear_conversion.machine_to_physics(4)
    machine_value = linear_conversion.physics_to_machine(5)
    assert physics_value == 11
    assert machine_value == 1


def test_quadratic_conversion():
    quadratic_conversion = UcPoly([1, 2, 3])
    physics_value = quadratic_conversion.machine_to_physics(4)
    assert physics_value == 27
    with pytest.raises(ValueError):
        quadratic_conversion.physics_to_machine(2.5)


def test_ppconversion_to_physics_2_points():
    pchip_uc = UcPchip([1, 3], [1, 3])
    assert pchip_uc.machine_to_physics(1) == 1
    assert pchip_uc.machine_to_physics(2) == 2
    assert pchip_uc.machine_to_physics(3) == 3


def test_pp_conversion_to_physics_3_points():
    pchip_uc = UcPchip([1, 3, 5], [1, 3, 6])
    assert pchip_uc.machine_to_physics(1) == 1
    assert np.round(pchip_uc.machine_to_physics(2), 4) == 1.8875
    assert pchip_uc.machine_to_physics(3) == 3
    assert np.round(pchip_uc.machine_to_physics(4), 4) == 4.3625
    assert pchip_uc.machine_to_physics(5) == 6


def test_pp_conversion_to_machine_2_points():
    pchip_uc = UcPchip([1, 3], [1, 3])
    assert pchip_uc.physics_to_machine(1) == 1
    assert pchip_uc.physics_to_machine(1.5) == 1.5

def test_pp_not_monotonely_increasing_error():
    with pytest.raises(ValueError):
        UcPchip([1, 2, 3], [1, 3, 2])

    with pytest.raises(ValueError):
        UcPchip([-1, -2, -3], [-1, -2, -3])
