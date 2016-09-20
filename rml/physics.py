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
    def __init__(self, voltage, frequency, harmonic_no):
        self.voltage = voltage
        self.frequency = frequency
        self.harmonic_no = harmonic_no
        self.time_lag = 0


class Ap(Physics):
    def __init__(self):
        self.limits = [0] * 4


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
        self.r1 = [[0 for x in range(6)] for y in range(6)]
        self.r2 = [[0 for x in range(6)] for y in range(6)]
        self.t1 = [0 for x in range(6)]
        self.t2 = [0 for x in range(6)]

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
    def __init__(self, entrance_angle, bending_angle, exit_angle, full_gap):
        self.entrance_angle = entrace_angle
        self.bending_angle = bending_angle
        self.exit_angle = exit_angle
        self.full_gap = full_gap
        self.fringe_int1 = 0
        self.fringe_int2 = 0


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
