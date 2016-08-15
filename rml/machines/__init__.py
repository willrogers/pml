import os
import sqlite3


def load_pvs(machine):
    basepath = os.path.dirname(__file__)
    filepath = os.path.abspath(os.path.join(basepath, machine, 'data.sqlite'))

    pv_names = []
    conn = sqlite3.connect(filepath)
    c = conn.cursor()

    c.execute('SELECT pv FROM pvs')
    while 1:
        row = c.fetchone()
        if not row:
            break
        pv_names.append(row)
    return pv_names
