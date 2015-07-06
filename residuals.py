#!/usr/bin/env python
# encoding: utf-8

import sys
import getopt
import re
import os
import pylab as plt
import numpy as np

# Define the variables for which the residuals will be plotted
variables = ["Ux", "Uy", "T", "p_rgh", "k", "epsilon"]

# Get the arguments of the script
def usage():
    print("Usage: residuals.py -l logfile\nPlot the residuals versus Time/Iteration")

try:
    options, args = getopt.getopt(sys.argv[1:], 'l:h', ['help', 'logfile='])
except getopt.GetoptError:
    usage()
    sys.exit(2)

for opt, arg in options:
    if opt in ("-l", "--logfile"):
        log_file = arg
    elif opt in ("-h", "--help"):
        usage()
        sys.exit(1)

# Get the lines of the logfile 'log_file'
lines = open(log_file, "r" ).readlines()

# Get the time and continuity values
time = [] # Time(s) or iterations counter
continuity = [] # Continuity values 
for line in lines:
    if re.search(r"^Time = ", line): # Search for string 'Time' at the begining of the line in file
        start = 'Time = '
        value = line.split(start)[1] # Take the Time value as the string just after start
        time.append(np.float(value)) # Transform the string in a float value
    elif re.search(r"continuity errors :", line): # Search for string 'continuity' in the lines of file 'log_file'
        start = 'sum local = '
        end = ', global'
        value = line.split(start)[1].split(end)[0] # Take the continuity value as string between start and end
        continuity.append(np.float(value)) # Transform the string in a float value

# Get the residual values for each variable
for variable in variables:
    data = []
    for line in lines:
        if re.search(r"Solving for " + variable, line):# Search for string variable in line of file 'log_file'
            start = 'Final residual = '
            end = ', No Iterations'
            value = line.split(start)[1].split(end)[0]
            data.append(np.float(value))
    plt.plot(np.array(time),np.array(data), label=variable) # Plot the residual values of variable

plt.plot(np.array(time),np.array(continuity), label="Continuity") # Plot the continuity values

# Plot
plt.title("Residuals plot:\n * logfile: " + log_file + "\n * case dir: " + os.getcwd().split('/')[-1], loc='left')
plt.xlabel("Time(s)/Iterations")
plt.ylabel("Residuals (Log Scale)")
plt.yscale('log')
plt.legend()
plt.grid()
plt.show()
