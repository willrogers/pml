import numpy as np
from scipy.interpolate import PchipInterpolator
from pml.exceptions import UniqueSolutionException


def unit_function(value):
    return value


class Uc(object):
    def __init__(self, f1=unit_function, f2=unit_function):
        self.f1 = f1
        self.f2 = f2

    def _machine_to_physics(self, value):
        raise NotImplementedError()

    def machine_to_physics(self, value):
        x = self._machine_to_physics(value)
        y = self.f1(x)
        return y

    def _physics_to_machine(self, value):
        raise NotImplementedError()

    def physics_to_machine(self, value):
        x = self._physics_to_machine(value)
        y = self.f2(x)
        return y


class UcPoly(Uc):
    def __init__(self, coef, f1=unit_function, f2=unit_function):
        """Linear interpolation for converting between physics and engineering units.

        Args:
            coef(array_like): The polynomial's coefficients, in decreasing powers.
        """
        super(self.__class__, self).__init__(f1, f2)
        self.p = np.poly1d(coef)

    def _machine_to_physics(self, machine_value):
        """Convert between machine and engineering units.

        Args:
            machine_value(float): The machine value to be converted to the engineering unit.

        Returns:
            float: The engineering value determined using the machine value.
        """
        return self.p(machine_value)

    def _physics_to_machine(self, physics_value):
        """Convert between engineering and machine units.

        Args:
            physics_value(float): The engineering value to be converted to the
                machine value.

        Returns:
            float: The converted machine value from the given engineering value.

        Raises:
            ValueError: An error occured when there exist no or more than one roots.
        """
        roots = (self.p - physics_value).roots
        if len(roots) == 1:
            x = roots[0]
            return x
        else:
            raise ValueError("There doesn't exist a corresponding machine value or "
                             "they are not unique:", roots)


class UcPchip(Uc):
    def __init__(self, x, y, f1=unit_function, f2=unit_function):
        """ PChip interpolation for converting between physics and engineering units.

        Args:
            x(list): A list of points on the x axis. These must be in increasing order
                for the interpolation to work. Otherwise, a ValueError is raised.
            y(list): A list of points on the y axis. These must be in increasing or
                decreasing order. Otherwise, a ValueError is raised.

        Raises:
            ValueError: An error occured when the given y coefficients are neither in
            increasing or decreasing order.
        """
        super(self.__class__, self).__init__(f1, f2)
        self.x = x
        self.y = y
        self.pp = PchipInterpolator(x, y)

        diff = np.diff(y)
        if not ((np.all(diff > 0)) or (np.all((diff < 0)))):
            raise ValueError("Given coefficients must be monotonically"
                             "decreasing.")

    def _machine_to_physics(self, machine_value):
        """Convert between machine and engineering units.

        Args:
            machine_value(float): The machine value to be converted to the engineering unit.
        Returns:
            float: The converted engineering value from the given machine value.
        """
        return self.pp(machine_value)

    def _physics_to_machine(self, physics_value):
        """Convert between engineering and machine units.

        Args:
            physics_value(float): The engineering value to be converted to the
                machine value.

        Returns:
            float: The converted engineering value from the given physics value.

        Raises:
            ValueError: An error occured when there exist no or more than one roots.
        """
        y = [val - physics_value for val in self.y]
        new_pp = PchipInterpolator(self.x, y)
        roots = new_pp.roots()
        if len(roots) == 1:
            x = roots[0]
            return x
        else:
            raise UniqueSolutionException("The function does not have any solution.")
