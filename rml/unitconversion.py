import numpy as np


class UnitConversion():
    def __init__(self, coef):
        self.p = np.poly1d(coef)

    def machine_to_physics(self, machine_value):
        return self.p(machine_value)

    def physics_to_machine(self, physics_value):
        roots = (self.p - physics_value).roots
        positive_roots = [root for root in roots if root > 0]
        if len(positive_roots) > 0:
            return positive_roots[0]
        else:
            raise ValueError("No corresponding positive machine value:", roots)
