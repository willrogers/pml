import numpy as np
from scipy.interpolate import PchipInterpolator


class UcPoly(object):
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


class UcPchip(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.pp = PchipInterpolator(x, y)

        diff = np.diff(y)
        if not (np.all(diff > 0)):
            raise ValueError('''Given coefficients must be
                                monotonely increasing.''')

    def machine_to_physics(self, machine_value):
        return self.pp(machine_value)

    def physics_to_machine(self, physics_value):
        y = [val - physics_value for val in self.y]
        new_pp = PchipInterpolator(self.x, y)
        return new_pp.roots()[0]
