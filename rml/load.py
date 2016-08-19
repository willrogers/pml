import os
import sqlite3
import csv
from rml.element import Element
from rml.lattice import Lattice


def load_lattice(load_dir):
    # Convert csv files into sqlite3 tables.
    # Pvs table: pv, elemName, elemHandle, elemField.
    # Elements table: elemName, elemType.
    con = sqlite3.connect(":memory:")
    cur = con.cursor()
    cur.execute("CREATE TABLE pvs (pv, elemName, elemHandle, elemField);")
    cur.execute("CREATE TABLE elements (elemName, elemType, elemLength);")

    pvs_db = []
    elem_db = []
    with open(load_dir + 'pvs.csv', 'rb') as fin:
        dr = csv.DictReader(fin)
        pvs_db = [(i['pv'], i['elemName'], i['elemHandle'],
                   i['elemField']) for i in dr]
    with open(load_dir + 'elements.csv', 'rb') as fin:
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
    for db_element in db_elements:
        id_ = db_element['elemName']
        fam = db_element['elemType']
        length = float(db_element['elemLength'])
        element = Element(id_, length=length)
        element.add_to_family(fam)

        cur.execute("select * from pvs where elemName='{}'".format(id_))
        matched_pvs = cur.fetchall()
        for pv in matched_pvs:
            pv_name = pv['pv']
            handle = pv['elemHandle']
            field = pv['elemField']
            element.put_pv_name(handle, field, pv_name)
        lattice.add_element(element)
    con.close()

    return lattice
