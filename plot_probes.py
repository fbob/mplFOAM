#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ************************************************
# Plot the probes signal written in the postProcessing/probes/0 directory
# It computes the number of probes and plot the signal(s) of field(s) at the probes.
# ************************************************

import os
import argparse
import numpy as np
import matplotlib.pyplot as plt 

def probes_nb(probes_path, field="U"):
    """Return the number of probes for each data field"""
    # Open the field probe file
    probe_file = open(probes_path + field, 'r')
    # Compute the number of probes nbProbes
    nb_probes = 0
    while probe_file.readline()[2] == "P" :
        nb_probes = nb_probes + 1
    # Close the probe file
    probe_file.close
    return nb_probes

def probes_fields(probes_path):
    """Give a list of all the fields present in the probes directory"""
    # WARNING: Add a test to check if the file is indeed a probe data file
    fields = []
    for (dirpath, dirnames, filenames) in os.walk(probes_path):
        fields.extend(filenames)
    return fields

def probes_coordinates(probes_path, nb_probes, field="U"):
    """Return the probes coordinates arrays"""
    # Open the field probe file
    probe_file=open(probes_path + field,'r')
    # Define the probes coordinates arrays
    xProbe = np.zeros(nb_probes) # Array of the x coordinates of all the probes
    yProbe = np.zeros(nb_probes) # Array of the y coordinates of all the probes
    zProbe = np.zeros(nb_probes) # Array of the z coordinates of all the probes
    for iProbe in range(0,nb_probes):
        lineStrings = probe_file.readline().split()
        xProbe[iProbe] = float(lineStrings[3][1:]) # Skip the first character which is '('
        yProbe[iProbe] = float(lineStrings[4])
        zProbe[iProbe] = float(lineStrings[5][:-1]) # Skip the last character which is ')'
    # Close the probe file
    probe_file.close
    return xProbe, yProbe, zProbe

def probes_data(probe_file, nb_probes, nb_components):
    """Return the probes data array"""
    # Distinguish the volVectorField and the volScalarField
    if nb_components==3:
        # Define the converters in order to convert string to float
        converters = {}
        k = 0
        for iProbe in range(0, nb_probes):
            converters[k+1] =  lambda s: float(s[1:])   # Skip the first character which is '('
            converters[k+3] =  lambda s: float(s[:-1])  # Skip the last character which is ')
            k = k + 3
        # Load the vector field values with loadtxt()
        data = np.loadtxt(probe_file, comments='#', delimiter=None ,converters=converters, unpack=True)

    elif nb_components==1:
        # Load scalar field values with loadtxt()
        data = np.loadtxt(probe_file, comments='#', delimiter=None ,converters=None, unpack=True)
    return data

# Path of the probes data
probes_path = "postProcessing/probes/0/"

# By default get all the fields present in the probe directory and set the nbProbes to its max
fields = probes_fields(probes_path)
nb_probes = probes_nb(probes_path)

# Create the parser
parser = argparse.ArgumentParser(
        description = "Plot fields signals versus Time/Iteration at choosen probes. If no probe and field are given all the probes will be plotted for all the fields.",
        epilog = "Happy Foaming ...")

parser.add_argument("-p", "--probes",
                    type = int,
                    nargs = "+",
                    default = range(nb_probes),
                    help="list of integers corresponding to the probes numbers")

parser.add_argument("-f", "--fields",
                    type = str,
                    nargs = "+",
                    default = fields,
                    help="list of string corresponding to the fields names")

# Get the args
args = parser.parse_args()
fields = args.fields # list of string: fields names
probes = args.probes # list of int: probes numbers 

# Define the fields type and the ones to plot
fieldsType={"U" : "volVectorField", "p" : "volScalarField", "T" : "volScalarField"}

# Get the coordinates of the probes
xProbe, yProbe, zProbe = probes_coordinates(probes_path,nb_probes)

# Loop over of the fields to plot
for iField in range(np.size(fields)):
    try:
        if fieldsType[fields[iField]] == "volVectorField":
            nb_components = 3
        elif fieldsType[fields[iField]] == "volScalarField":
            nb_components = 1
    except:
        print "Error: One of the field to plot has a unknown fieldType"
        exit

    # Open the probe file
    probe_file=open(probes_path + fields[iField],'r')

    # Get the probes data
    data = probes_data(probe_file, nb_probes, nb_components)

    # Creation of the different figures
    f1 = plt.figure()
    nb_probes_to_plot = np.size(probes)
    for i in range(nb_probes_to_plot):
        iProbe = probes[i]
        for j in range(nb_components):
            ax = f1.add_subplot(nb_probes_to_plot,nb_components,nb_components*i + j + 1)
            ax.set_title(r'Point '+ str(iProbe) + str(" (%.3f %.3f %.3f)"% (xProbe[iProbe],yProbe[iProbe],zProbe[iProbe])),fontsize=12)
            x = data[0,:]
            y = data[nb_components*i + j + 1,:]
            # Change the labels of the axes according to the number of components
            if nb_components == 3:
                label = r'$'+fields[iField]+'_'+str(j)+'$'
                ax.set_ylabel(r'$'+fields[iField]+'_'+str(j)+'$')
            elif nb_components == 1:
                label = r'$'+fields[iField]+'$'
                ax.set_ylabel(r'$'+fields[iField]+'$')
            ax.set_xlabel(r'Time$(\Delta t)$')
            ax.plot(x,y,lw=2, ms=5,label= label)
            ax.xaxis.grid(True)
            ax.yaxis.grid(True)
            ax.legend(loc='best')
    plt.tight_layout(pad=0.01)

# Draw the figures
plt.show()
