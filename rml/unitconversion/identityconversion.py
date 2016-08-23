'''
Default unit conversion object used for an element
'''


class IdentityConversion():
    def __init__(self):
        pass

    def machine_to_physics(self, machine_value):
        physics_value = machine_value
        return physics_value

    def physics_to_machine(self, physics_value):
        machine_value = physics_value
        return machine_value
