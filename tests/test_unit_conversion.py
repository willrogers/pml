import pytest
from rml.unitconversion import UnitConversion


def test_identity_conversion():
    id_conversion = UnitConversion([1, 0])
    physics_value = id_conversion.machine_to_physics(4)
    machine_value = id_conversion.physics_to_machine(4)
    assert machine_value == 4
    assert physics_value == 4


def test_linear_conversion():
    linear_conversion = UnitConversion([2, 3])
    physics_value = linear_conversion.machine_to_physics(4)
    machine_value = linear_conversion.physics_to_machine(5)
    assert physics_value == 11
    assert machine_value == 1


def test_quadratic_conversion():
    quadratic_conversion = UnitConversion([1, 2, 3])
    physics_value = quadratic_conversion.machine_to_physics(4)
    assert physics_value == 27
    with pytest.raises(ValueError):
        quadratic_conversion.physics_to_machine(2.5)
