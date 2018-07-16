This repository contains some Python functions to plot OpenFOAM data with Matplotlib.

mplFOAM
=======

This module contains functions to plot OpenFOAM data with Matplotlib using paraview.simple and numpy_support from vtk.util.

At present time it only support:
* surface plot in slice
* plot along line

plot_probes
===========

This command line utility plots the probes signals written in the postProcessing/probes/0 directory
It computes the number of probe(s) and plot the field(s) signal(s) at the probes.

```bash
Usage: plot_probes.py [-h] [-p PROBES [PROBES ...]] [-f FIELDS [FIELDS ...]]

Plot fields signals versus Time/Iteration at choosen probes. 
If no probe and field are given all the probes will be plotted for all the fields.

optional arguments:
  -h, --help            show this help message and exit
  -p PROBES [PROBES ...], --probes PROBES [PROBES ...]
                        list of integers corresponding to the probes numbers
  -f FIELDS [FIELDS ...], --fields FIELDS [FIELDS ...]
                        list of string corresponding to the fields names
```

For example, the command line invocation:
```bash
plot_probes.py -f U p -p 0 1
```
will produce

![U field signals](/screenshots/U_field_probes-0-1.png)
![p field signals](/screenshots/p_field_probes-0-1.png)
