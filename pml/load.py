'''
Load the lattice given loading directory which contains two .txt files
containing the pvs and the elements of the lattice. Files used for SRI21
are dumped from a .sqlite database.
TODO: split the code in sub methods
      look into quicker way to load the elements from memory
      not sure whether load_lattice should have a cs and uc parameter
      part where a device is created is rather complicated
'''
import sqlite3
import csv
import io
import pml.physics
from pml.element import Element
from pml.lattice import Lattice
from pml.device import Device
from pml.units import UcPoly
from pml.cs_dummy import CsDummy


PHYSICS_CLASSES = {'RF': pml.physics.Rf,
                   'AP': pml.physics.Ap,
                   'DRIFT': pml.physics.Drift,
                   'BPM': pml.physics.Bpm,
                   'BEND': pml.physics.Bend,
                   'QUAD': pml.physics.Quad,
                   'SEXT': pml.physics.Sext,
                   'DIPOLE': pml.physics.Dipole,
                   'HSTR': pml.physics.Hstr,
                   'VSTR': pml.physics.Vstr,
                   'VTRIM': pml.physics.Vtrim,
                   'HTRIM': pml.physics.Htrim,
                   'MPW12': pml.physics.Mpw12,
                   'MPW15': pml.physics.Mpw15,
                   'BPM10': pml.physics.Bpm10,
                   'source': pml.physics.Source,
                   'HCHICA': pml.physics.Hchica}


def load_lattice(load_dir, cs=CsDummy(), uc=UcPoly([1, 0])):
    # Convert csv files into sqlite3 tables.
    # Pvs table: pv, elemName, elemHandle, elemField.
    # Elements table: elemName, elemType.
    con = sqlite3.connect(":memory:")
    cur = con.cursor()
    cur.execute("CREATE TABLE pvs (pv, elemName, elemHandle, elemField);")
    cur.execute("""CREATE TABLE elements (elemName, elemType, elemLength,
    elemGroups);""")

    pvs_db = []
    elem_db = []
    with io.open(load_dir + 'pvs.csv', 'r') as fin:
        dr = csv.DictReader(fin)
        pvs_db = [(i['pv'], i['elemName'], i['elemHandle'],
                   i['elemField']) for i in dr]
    with io.open(load_dir + 'elements.csv', 'r') as fin:
        dr = csv.DictReader(fin)
        elem_db = [(i['elemName'], i['elemType'], i['elemLength'],
                    i['elemGroups']) for i in dr]
    cur.executemany("INSERT INTO pvs (pv, elemName, elemHandle, elemField)\
    VALUES (?, ?, ?, ?);", pvs_db)
    cur.executemany("INSERT INTO elements (elemName, elemType, elemLength, elemGroups)\
    VALUES (?, ?, ?, ?);", elem_db)
    con.commit()

    # Store db elements in an array and use it to match pvs to an element
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    lattice = Lattice('SRI21')

    cur.execute("select * from elements left outer join pvs on elements.elemName = pvs.elemName")
    db_elements = cur.fetchall()

    # Go through the database and create elements
    created_elements = {}
    for i, db_element in enumerate(db_elements):
        id_ = db_element['elemName']
        try:
            element = created_elements[id_]
        except KeyError:
            _type = db_element['elemType']
            length = float(db_element['elemLength'])
            family = db_element['elemGroups']
            physics = PHYSICS_CLASSES[_type](length)
            element = Element(id_, _type, physics)
            element.add_to_family(_type)
            element.add_to_family(family)
            lattice.add_element(element)
            created_elements[id_] = element

        # Now create devices if necessary.
        field = db_element['elemField']

        if field is not None:
            pv = db_element['pv']
            handle = db_element['elemHandle']
            rb_pv = pv if handle == 'get' else None
            sp_pv = pv if handle == 'put' else None
            try:
                device = element.devices[field]
                if rb_pv is not None:
                    device.rb_pv = rb_pv
                if sp_pv is not None:
                    device.sp_pv = sp_pv
            except KeyError:
                device = Device(rb_pv, sp_pv, cs)
                element.devices[field] = device
    con.close()

    return lattice
