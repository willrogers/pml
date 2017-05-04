import os
import csv
from pml import lattice, element, device, units
import collections


def load_unitconv(directory, mode, lattice):
    data = collections.defaultdict(list)
    uc = {}
    with open(os.path.join(directory, mode, 'uc_poly_data.csv')) as poly:
        csv_reader = csv.DictReader(poly)
        for item in csv_reader:
            data[(int(item['uc_id']))].append((int(item['coeff']), float(item['val'])))

    for d in data:
        u = units.UcPoly([x[1] for x in reversed(sorted(data[d]))])
        uc[d] = u
    data.clear()
    with open(os.path.join(directory, mode, 'uc_pchip_data.csv')) as pchip:
        csv_reader = csv.DictReader(pchip)
        for item in csv_reader:
            data[(int(item['uc_id']))].append((float(item['eng']), float(item['phy'])))

    for d in data:
        eng = [x[0] for x in sorted(data[d])]
        phy = [x[1] for x in sorted(data[d])]
        u = units.UcPchip(eng, phy)
        uc[d] = u

    with open(os.path.join(directory, mode, 'unitconv.csv')) as unitconv:
        csv_reader = csv.DictReader(unitconv)
        for item in csv_reader:
            element = lattice[int(item['el_id']) - 1]
            element._uc[item['field']] = uc[int(item['uc_id'])]


def load(directory, mode, control_system):
    lat = lattice.Lattice(mode, control_system)
    with open(os.path.join(directory, mode, 'elements.csv')) as elements:
        csv_reader = csv.DictReader(elements)
        for item in csv_reader:
            e = element.Element(item['name'], float(item['length']),
                                item['type'], None)
            e.add_to_family(item['type'])
            lat.add_element(e)

    with open(os.path.join(directory, mode, 'devices.csv')) as devices:
        csv_reader = csv.DictReader(devices)
        for item in csv_reader:
            d = device.Device(None, item['get_pv'], item['set_pv'])
            lat[int(item['id']) - 1].add_device(item['field'], d, None)

    with open(os.path.join(directory, mode, 'families.csv')) as families:
        csv_reader = csv.DictReader(families)
        for item in csv_reader:
            lat[int(item['id']) - 1].add_to_family(item['family'])

    if os.path.exists(os.path.join(directory, mode, 'unitconv.csv')):
        load_unitconv(directory, mode, lat)

    return lat
