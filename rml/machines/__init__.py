import os
import sqlite3
from rml.element import Element
from rml.lattice import Lattice


def load():
    '''
    Not implemented. Will load the machine here instead of using machine
    parameter in get_elements()
    '''
    pass


def get_elements(machine, elemType='BPM'):
    basepath = os.path.dirname(__file__)
    filepath = os.path.abspath(os.path.join(basepath, machine, 'data.sqlite'))

    conn = sqlite3.connect(filepath)
    c = conn.cursor()
    c.execute('SELECT * FROM elements WHERE elemType=\'' + elemType + '\';')

    lattice = Lattice('SRI21')
    while 1:
        row = c.fetchone()
        if not row:
            break
        el_name = row[1]
        el_type = row[2]
        element = Element(el_name, el_type)
        lattice.add_element(element)
    return lattice
