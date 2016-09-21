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
import rml.physics
from rml.element import Element
from rml.lattice import Lattice
from rml.device import Device
from rml.units import UcPoly
from rml.cs_dummy import CsDummy


PHYSICS_CLASSES = {'RF': rml.physics.Rf,
                   'AP': rml.physics.Ap,
                   'DRIFT': rml.physics.Drift,
                   'BPM': rml.physics.Bpm,
                   'BEND': rml.physics.Bend,
                   'QUAD': rml.physics.Quad,
                   'SEXT': rml.physics.Sext,
                   'DIPOLE': rml.physics.Dipole,
                   'HSTR': rml.physics.Hstr,
                   'VSTR': rml.physics.Vstr,
                   'VTRIM': rml.physics.Vtrim,
                   'HTRIM': rml.physics.Htrim,
                   'MPW12': rml.physics.Mpw12,
                   'MPW15': rml.physics.Mpw15,
                   'BPM10': rml.physics.Bpm10,
                   'source': rml.physics.Source,
                   'AP': rml.physics.Ap,
                   'HCHICA': rml.physics.Hchica}


def load_lattice(load_dir, cs=CsDummy(), uc=UcPoly([1, 0])):
    # Convert csv files into sqlite3 tables.
    # Pvs table: pv, elemName, elemHandle, elemField.
    # Elements table: elemName, elemType.
    con = sqlite3.connect(":memory:")
    cur = con.cursor()
    cur.execute("CREATE TABLE pvs (pv, elemName, elemHandle, elemField);")
    cur.execute("CREATE TABLE elements (elemName, elemType, elemLength);")

    pvs_db = []
    elem_db = []
    with io.open(load_dir + 'pvs.csv', 'r') as fin:
        dr = csv.DictReader(fin)
        pvs_db = [(i['pv'], i['elemName'], i['elemHandle'],
                   i['elemField']) for i in dr]
    with io.open(load_dir + 'elements.csv', 'r') as fin:
        dr = csv.DictReader(fin)
        elem_db = [(i['elemName'], i['elemType'], i['elemLength']) for i in dr]
    cur.executemany("INSERT INTO pvs (pv, elemName, elemHandle, elemField)\
    VALUES (?, ?, ?, ?);", pvs_db)
    cur.executemany("INSERT INTO elements (elemName, elemType, elemLength)\
    VALUES (?, ?, ?);", elem_db)
    con.commit()

    # Store db elements in an array and use it to match pvs to an element
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    lattice = Lattice('SRI21')

    cur.execute("select * from elements")
    db_elements = cur.fetchall()
    cur.execute("select distinct elemField from pvs;")
    fields = cur.fetchall()
    # Go through the database and create elements
    for db_element in db_elements:
        id_ = db_element['elemName']
        fam = db_element['elemType']
        length = float(db_element['elemLength'])
        physics = PHYSICS_CLASSES[fam](length)
        element = Element(id_, physics)
        element.add_to_family(fam)

        # Add devices to an element
        for field in fields:
            cur.execute("""select * from (select * from pvs where elemName='{0}')
            where elemField like '{1}'""".format(id_, field['elemField']))
            matched_pvs = cur.fetchall()
            if len(matched_pvs) > 0:
                d = dict()
                for pv in matched_pvs:
                    handle = pv['elemHandle']
                    if handle == 'get':
                        d['get'] = pv['pv']
                    elif handle == 'put':
                        d['put'] = pv['pv']
                    device = Device(d.get('get', ''), d.get('put', ''),
                                    cs=cs)
                    element.add_device(field[0], device, uc)
        lattice.add_element(element)
    con.close()

    return lattice
