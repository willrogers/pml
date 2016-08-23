''' Linear conversion between machine and physics values '''


class LinearConversion():

    def __init__(self, first_coefficient, second_coefficent):
        self.A = first_coefficient
        self.B = second_coefficent

    def machine_to_physics(self, machine_value):
        physics_value = self.A * machine_value + self.B
        return physics_value

    def physics_to_machine(self, physics_value):
        machine_value = (physics_value - self.B)/self.A
        return machine_value
