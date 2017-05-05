import numpy as np
from scipy.interpolate import PchipInterpolator
from pml.exceptions import UniqueSolutionException


class UcPoly(object):
    ''' Linear interpolation for converting between physics and engineering units.'''
    def __init__(self, coef):
        '''
        Takes a list of coefficients and interpolates them using linear interpolation.
        '''
        self.p = np.poly1d(coef)

    def machine_to_physics(self, machine_value):
        '''
        Given machine value find out the engineering value.
        '''
        return self.p(machine_value)

    def physics_to_machine(self, physics_value):
        '''
        Given engineering value find out the machine value.
        '''
        roots = (self.p - physics_value).roots
        if len(roots) == 1:
            return roots[0]
        else:
            raise ValueError("""There doesn't exist a corresponding machine value or
                              they are not unique:""", roots)


class UcPchip(object):
    '''
    PChip interpolation for converting between physics and engineering units.
    The y coefficients must be in monotonically increasing order for the inverse
    to have unique values.
    '''
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.pp = PchipInterpolator(x, y)

        raiseException = False;
        diff = np.diff(y)
        if not ((np.all(diff > 0)) or (np.all((diff < 0)))):
            raise ValueError('''Given coefficients must be monotonically
                                decreasing.''')

    def machine_to_physics(self, machine_value):
        '''
        Given machine value find out the engineering value.
        '''
        return self.pp(machine_value)

    def physics_to_machine(self, physics_value):
        '''
        Given engineering value find out the machine value.
        '''
        y = [val - physics_value for val in self.y]
        new_pp = PchipInterpolator(self.x, y)
        roots = new_pp.roots()
        if(len(roots) == 1):
            return roots[0]
        else:
            raise UniqueSolutionException("The function does not have any solution.")
