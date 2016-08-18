import os
import sqlite3
from rml.element import Element
from rml.lattice import Lattice
from rml.utility import binary_search


def get_elements(machine, element_type):
    basepath = os.path.dirname(__file__)
    filepath = os.path.abspath(os.path.join(basepath, machine, 'data.sqlite'))

    # Load data from the elements table
    conn = sqlite3.connect(filepath)
    c = conn.cursor()
    c.execute('SELECT * FROM elements WHERE elemType=\'' + element_type + '\';')

    lattice = Lattice(machine)
    while 1:
        row = c.fetchone()
        if not row:
            break
        el_name = row[1]
        el_type = row[2]
        element = Element(el_name, el_type)
        lattice.add_element(element)

    # Parse the pvs from the pv table
    conn = sqlite3.connect(filepath)
    c = conn.cursor()
    c.execute('SELECT * FROM pvs;')

    while 1:
        row = c.fetchone()
        if not row:
            break
        pv = row[1]
        pv_id = row[2]
        pv_handle = row[3]
        pv_field = row[4]
        elements = lattice.get_elements()
        found = binary_search(elements, pv_id)
        if found:
            if pv_handle == 'get':
                elements[found].put_pv_name('readback', pv_field, pv)
            elif pv_handle == 'put':
                elements[found].put_pv_name('setpoint', pv_field, pv)
            elements[found].has_pv = True

    return lattice
