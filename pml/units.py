import numpy as np
from scipy.interpolate import PchipInterpolator
from pml.exceptions import UniqueSolutionException


def unit_function(value):
    return value


class UnitConv(object):
    def __init__(self, f1=unit_function, f2=unit_function):
        self.f1 = f1
        self.f2 = f2

    def _raw_eng_to_phys(self, value):
        raise NotImplementedError()

    def eng_to_phys(self, value):
        x = self._raw_eng_to_phys(value)
        y = self.f1(x)
        return y

    def _raw_phys_to_eng(self, value):
        raise NotImplementedError()

    def phys_to_eng(self, value):
        x = self._raw_phys_to_eng(value)
        y = self.f2(x)
        return y


class PolyUnitConv(UnitConv):
    def __init__(self, coef, f1=unit_function, f2=unit_function):
        """Linear interpolation for converting between physics and engineering units.

        Args:
            coef(array_like): The polynomial's coefficients, in decreasing powers.
        """
        super(self.__class__, self).__init__(f1, f2)
        self.p = np.poly1d(coef)

    def _raw_eng_to_phys(self, eng_value):
        """Convert between engineering and physics units.

        Args:
            eng_value(float): The engineering value to be converted to the engineering unit.

        Returns:
            float: The physics value determined using the engineering value.
        """
        return self.p(eng_value)

    def _raw_phys_to_eng(self, physics_value):
        """Convert between physics and engineering units.

        Args:
            physics_value(float): The physics value to be converted to the
                engineering value.

        Returns:
            float: The converted engineering value from the given physics value.

        Raises:
            ValueError: An error occured when there exist no or more than one roots.
        """
        roots = (self.p - physics_value).roots
        if len(roots) == 1:
            x = roots[0]
            return x
        else:
            raise ValueError("There doesn't exist a corresponding engineering value or "
                             "they are not unique:", roots)


class PchipUnitConv(UnitConv):
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

    def _raw_eng_to_phys(self, eng_value):
        """Convert between engineering and physics units.

        Args:
            eng_value(float): The engineering value to be converted to the engineering unit.
        Returns:
            float: The converted engineering value from the given engineering value.
        """
        return self.pp(eng_value)

    def _raw_phys_to_eng(self, physics_value):
        """Convert between physics and engineering units.

        Args:
            physics_value(float): The engineering value to be converted to the
                engineering value.

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
