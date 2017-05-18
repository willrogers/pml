Examples
********

Print BPM pvs along with s position
-----------------------------------

- Print all bpms along with their readback pvs and position in the ring::
    $ ipython
- Import 'pml'

     >>> import pml.load_csv
     >>> import epics.cs

- Initialize the VMX mode

     >>> lattice = pml.load_csv.load('/home/cxa78676/pml/pml/data/', 'VMX', epics.cs.EpicsControlSystem())

- Get the BPM elements

     >>> bpms = lattice.get_elements('BPM')

- Print the values of the readback pvs on the b1 field

     >>> for bpm in bpms:
     >>>    print(bpm.get_pv_name('x', 'readback'), bpm.get_pv_name('y', 'readback'), 'S position', lattice.get_s(bpm))

Get the pv value from the quad elements
---------------------------------------

- Enter IPpython::
    $ ipython
- Import 'pml'

     >>> import pml

- Initialize the VMX mode

     >>> lattice = pml.load_csv.load('/home/cxa78676/pml/pml/data/', 'VMX', epics.cs.EpicsControlSystem())

- Get the Quad elements

     >>> quads = lattice.get_elements('QUAD')

- Print the values of the readback pvs on the b1 field

     >>> for quad in quads:
     >>>    print(quad.get_pv_value('b1', 'readback'))

Print pv names to file
----------------------

- Enter IPpython::
    $ ipython
- Import 'pml' and epics

     >>> import pml.load_csv
     >>> import epics.cs

- Initialize the VMX mode

     >>> lattice = pml.load_csv.load('/home/cxa78676/pml/pml/data/', 'VMX', epics.cs.EpicsControlSystem())

- Get the Quad elements

     >>> q1b = lattice.get_elements('Q1B')

- Print the pvs to file

     >>> with open('elements_in_families.txt', 'a') as out_file:
     >>>    for quad in q1b:
     >>>       pv_name = element.get_pv_name('b1', 'readback').split(':')[0]
     >>>       out_file.write("{}\n".format(pv_name))
