#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ************************************************
# Plot the probes signal written in the postProcessing/probes/0 directory
# It computes the number of probes and plot the signal
# of a field at the probes in a figure
# ************************************************

import os
import argparse
import numpy as np
import matplotlib.pyplot as plt 

# Function which gets the numbers of probes present for each data field
def probes_nb(probes_path, field="U"):
    # Open the field probe file
    probeFile=open(probes_path + field, 'r')
    # Compute the number of probes nbProbes
    nbProbes = 0
    while probeFile.readline()[2] == "P" :
        nbProbes = nbProbes + 1
    # Close the probe file
    probeFile.close
    return nbProbes

# Function which list all the fields present in the probes directory
def probes_fields(probes_path):
    """Give a list of all the fields present in the probes directory"""
    # WARNING: Add a test to check if the file is indeed a probe data file
    fields = []
    for (dirpath, dirnames, filenames) in os.walk(probes_path):
        fields.extend(filenames)
    return fields

# Function which return the probes coordinates
def probes_coordinates(probes_path, nbProbes, field="U"):
    """Return the probes coordinates arrays"""
    # Open the field probe file
    probeFile=open(probes_path + field,'r')
    # Define the probes coordinates arrays
    xProbe = np.zeros(nbProbes) # Array of the x coordinates of all the probes
    yProbe = np.zeros(nbProbes) # Array of the y coordinates of all the probes
    zProbe = np.zeros(nbProbes) # Array of the z coordinates of all the probes
    for nbProbe in range(0,nbProbes):
        lineStrings = probeFile.readline().split()
        xProbe[nbProbe] = float(lineStrings[3][1:]) # Skip the first character which is '('
        yProbe[nbProbe] = float(lineStrings[4])
        zProbe[nbProbe] = float(lineStrings[5][:-1]) # Skip the last character which is ')'
    # Close the probe file
    probeFile.close
    return xProbe, yProbe, zProbe

# Function which return the probes data
def probes_data(probeFile, nbProbes, nbComponents):
    """Return the probes data array"""
    # Distinguish the volVectorField and the volScalarField
    if nbComponents==3:
        # Define the converters in order to convert string to float
        converters = {}
        k = 0
        for i in range(0, nbProbes):
            converters[k+1] =  lambda s: float(s[1:])   # Skip the first character which is '('
            converters[k+3] =  lambda s: float(s[:-1])  # Skip the last character which is ')
            k = k + 3
        # Load the vector field values with loadtxt()
        data = np.loadtxt(probeFile, comments='#', delimiter=None ,converters=converters, unpack=True)

    elif nbComponents==1:
        # Load scalar field values with loadtxt()
        data = np.loadtxt(probeFile, comments='#', delimiter=None ,converters=None, unpack=True)
    return data

# Path of the probes data
probes_path = "postProcessing/probes/0/"

# By default get all the fields present in the probe directory and set the nbProbes to its max
fields = probes_fields(probes_path)
nbProbes = probes_nb(probes_path)

# Create the parser
parser = argparse.ArgumentParser(
        description = "Plot fields signals versus Time/Iteration at choosen probes. If no probe and field are given all the probes will be plotted for all the fields.",
        epilog = "Happy Foaming ...")

parser.add_argument("-p", "--probes",
                    type = int,
                    nargs = "+",
                    default = range(nbProbes),
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
xProbe, yProbe, zProbe = probes_coordinates(probes_path,nbProbes)

# Loop over of the fields to plot
for iField in range(np.size(fields)):
    try:
        if fieldsType[fields[iField]] == "volVectorField":
            nbComponents = 3
        elif fieldsType[fields[iField]] == "volScalarField":
            nbComponents = 1
    except:
        print "Error: One of the field to plot has a unknown fieldType"
        exit

    # Open the probe file
    probeFile=open(probes_path + fields[iField],'r')

    # Get the probes data
    data = probes_data(probeFile, nbProbes, nbComponents)

    #
    # Creation of the different figures
    #
    f1 = plt.figure()
    nb_probes_to_plot = np.size(probes)
    for i in range(nb_probes_to_plot):
        iProbe = probes[i]
        for j in range(nbComponents):
            ax = f1.add_subplot(nb_probes_to_plot,nbComponents,nbComponents*i + j + 1)
            ax.set_title(r'Point '+ str(iProbe) + str(" (%.3f %.3f %.3f)"% (xProbe[iProbe],yProbe[iProbe],zProbe[iProbe])),fontsize=12)
            x = data[0,:]
            y = data[nbComponents*i + j + 1,:]
            # Change the labels of the axes according to the number of components
            if nbComponents == 3:
                label = r'$'+fields[iField]+'_'+str(j)+'$'
                ax.set_ylabel(r'$'+fields[iField]+'_'+str(j)+'$')
            elif nbComponents == 1:
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
