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

    with open(os.path.join(directory, 'devices.csv')) as elements:
        csv_reader = csv.DictReader(elements)
        for item in csv_reader:
            d = device.Device(None, item['get_pv'], item['get_pv'])
            lat[int(item['id']) - 1].add_device(item['field'], d, None)

    return lat
