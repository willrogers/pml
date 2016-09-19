'''
Other element types available in MML:
HCHICA
VTRIM
HTRIM
MPW12
MPW15
BPM10
source
'''
from rml.device import Device


class Physics(object):
    def __init__(self, length=0):
        self.length = length

    def get_value(self, field, handle):
        raise NotImplementedError('''This method should be overwritten
                                     in children classes!''')

    def put_value(self, field, unit):
        raise NotImplementedError('''This method should be overwritten
                                     in children classes!''')


class Rf(Physics):
    def __init__(self):
        pass


class Ap(Physics):
    def __init__(self):
        pass


class Drift(Physics):
    def __init__(self):
        pass


class Bpm(Physics):
    def __init__(self):
        pass

    def get_x(self):
        pass

    def get_y(self):
        pass


# Magnets
class Magnet(Physics):
    # Should create subclasses of each magnet that inherit MagnetPhysics
    # Quad, dipole, corrector, sext
    def __init__(self, poly_a, poly_b):
        self.poly_a = poly_a
        self.poly_b = poly_b

    def put_b2(self, value, unit):
        pass

    def get_b2(self, value, unit):
        pass


class Bend(Magnet):
    pass


class Quad(Magnet):
    def __init__(self, ):
        pass

    def put_b1(self, ):
        pass

    def get_b1(self):
        pass


class Sext(Magnet):
    def __init__(self):
        pass

    def put_b2(self):
        pass

    def get_b2(self):
        pass


class Dipole(Magnet):
    def __init__(self, gap, bending_angle):
        self.gap = gap
        self.bending_angle = bending_angle


# Correctors
class Corrector(Magnet):
    def __init__(self):
        pass

    def put_b0(self):
        pass

    def get_b0(self):
        pass


class Hstr(Corrector):
    pass


class Vstr(Corrector):
    pass
