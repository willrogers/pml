import os
import csv
from pml import lattice, element, device


def load(directory):
    lat = lattice.Lattice('dummy')
    with open(os.path.join(directory, 'elements.csv')) as elements:
        csv_reader = csv.DictReader(elements)
        for item in csv_reader:
            e = element.Element(item['name'], float(item['length']),
                                item['type'], None)
            e.add_to_family(item['type'])
            lat.add_element(e)

    with open(os.path.join(directory, 'devices.csv')) as devices:
        csv_reader = csv.DictReader(devices)
        for item in csv_reader:
            d = device.Device(None, item['get_pv'], item['set_pv'])
            lat[int(item['id']) - 1].add_device(item['field'], d, None)

    with open(os.path.join(directory, 'families.csv')) as families:
        csv_reader = csv.DictReader(families)
        for item in csv_reader:
            lat[int(item['id']) - 1].add_to_family(item['family'])

    return lat
