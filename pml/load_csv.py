import os
import csv
from pml import lattice, element, device


def load(mode, control_system, directory=None):
    '''
    Load a lattice object from a directory.

    Parameters:
      mode: the mode to be loaded
      control_system: control system to be used
      directory: directory where to load the files from. If no directory is
          given that the data directory at the root of the repository is used.
    '''
    if directory is None:
        directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
    lat = lattice.Lattice(mode, control_system, 1)
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
            d = device.Device(control_system, item['get_pv'], item['set_pv'])
            lat[int(item['id']) - 1].add_device(item['field'], d, None)

    with open(os.path.join(directory, mode, 'families.csv')) as families:
        csv_reader = csv.DictReader(families)
        for item in csv_reader:
            lat[int(item['id']) - 1].add_to_family(item['family'])

    return lat
