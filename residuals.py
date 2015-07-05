#!/usr/bin/env python
# encoding: utf-8

# Imports
import sys
import getopt
import re
import os
import pylab as pl
import numpy as np
from matplotlib.legend_handler import HandlerLine2D


# Get the arguments of the script
def usage():
    print("Usage: residuals.py -l logfile\nPlot the residuals versus Time/Iteration")

try:
    options, args = getopt.getopt(sys.argv[1:], 'l:h', ['help', 'logfile='])
    print("Options:",options)
    print("Args:",args)
except getopt.GetoptError:
    usage()
    sys.exit(2)

for opt, arg in options:
    if opt in ("-l", "--logfile"):
        log_file = arg
        print("Log file is:",log_file)
    elif opt in ("-h", "--help"):
        usage()
        sys.exit(1)

lines = open(log_file, "r" ).readlines()

variables = ["Ux", "Uy", "Uz","k","w","e","p","time"]

# If the residuals files exist remove them
for variable in variables:
    filename = variable + "_" + log_file
    if os.path.isfile(filename):
        os.remove(filename)

# search for specific parts of input file and paste in output file (loop)
for line in lines:
    if re.search( r"Solving for Ux", line ):# Searching for Ux line in file
        if not os.path.isfile("Ux_" + log_file):# if there is not a Ux text file make one
            fileUx = open("Ux_" + log_file, 'w')
            fileUx.write('Ux \n')
        start = 'Final residual = '
        end = ', No Iterations'
        Ux = line.split(start)[1].split(end)[0]# take residual as string between start and end
        fileUx.write(Ux + '\n')

    elif re.search( r"Solving for Uy", line ):
        if not os.path.isfile("Uy_" + log_file):
            fileUy = open("Uy_" + log_file, 'w')
            fileUy.write('Uy \n')
        start = 'Final residual = '
        end = ', No Iterations'
        Uy = line.split(start)[1].split(end)[0]
        fileUy.write(Uy + '\n')

    elif re.search( r"Solving for Uz", line ):
        if not os.path.isfile("Uz_" + log_file):
            fileUz = open("Uz_" + log_file, 'w')
            fileUz.write('Uz \n')
        start = 'Final residual = '
        end = ', No Iterations'
        Uz = line.split(start)[1].split(end)[0]
        fileUz.write(Uz + '\n')

    elif re.search( r"Solving for p", line ):
        if not os.path.isfile("p_" + log_file):
            filep = open("p_" + log_file, 'w')
            filep.write('p \n')
        start = 'Final residual = '
        end = ', No Iterations'
        p = line.split(start)[1].split(end)[0]
        filep.write(p + '\n')

    elif re.search( r"Solving for omega", line ):
        if not os.path.isfile("w_" + log_file):
            filew = open("w_" + log_file, 'w')
            filew.write('w \n')
        start = 'Final residual = '
        end = ', No Iterations'
        w = line.split(start)[1].split(end)[0]
        filew.write(w + '\n')

    elif re.search( r"Solving for k", line ):
        if not os.path.isfile("k_" + log_file):
            filek = open("k_" + log_file, 'w')
            filek.write('k \n')
        start = 'Final residual = '
        end = ', No Iterations'
        k = line.split(start)[1].split(end)[0]
        filek.write(k + '\n')

    elif re.search( r"Solving for epsilon", line ):
        if not os.path.isfile("e_" + log_file):
            filee = open("e_" + log_file, 'w')
            filee.write('e \n')
        start = 'Final residual = '
        end = ', No Iterations'
        e = line.split(start)[1].split(end)[0]
        filee.write(e + '\n')

    elif re.search( r"Time = ", line ):
        if not os.path.isfile("time_" + log_file):
            filetime = open("time_" + log_file, 'w')
            filetime.write('time \n')
        if not re.search( r"ClockTime =", line ):
            start = 'Time = '
            time = line.split(start)[1]
            filetime.write(time)

# if output files exist close them, then setup graph parameters by outputting list
if os.path.isfile("time_" + log_file):# if Ux file exists close it
        filetime.close()
        datatime=np.genfromtxt("time_" + log_file , skiprows=2)# describes data for time
if os.path.isfile("Ux_" + log_file):
        fileUx.close()
        dataUx=np.genfromtxt("Ux_" + log_file , skiprows=2)
        line1, = pl.plot(datatime,dataUx,'',label = "Ux" ,linewidth=1)
if os.path.isfile("Uy_" + log_file):
        fileUy.close()
        dataUy=np.genfromtxt("Uy_" + log_file , skiprows=2)
        line2, = pl.plot(datatime,dataUy,'',label = "Uy" ,linewidth=1)
if os.path.isfile("Uz_" + log_file):
        fileUz.close()
        dataUz=np.genfromtxt("Uz_" + log_file , skiprows=2)
        line3, = pl.plot(datatime,dataUz,'',label = "Uz" ,linewidth=1)
if os.path.isfile("p_" + log_file):
        filep.close()
        datap=np.genfromtxt("p_" + log_file , skiprows=2)
        line4, = pl.plot(datatime,datap,'',label = "p" ,linewidth=1)
if os.path.isfile("k_" + log_file):
        filek.close()
        datak=np.genfromtxt("k_" + log_file , skiprows=2)
        line5, = pl.plot(datatime,datak,'',label = "k" ,linewidth=1)
if os.path.isfile("w_" + log_file):
        filew.close()
        dataw=np.genfromtxt("w_" + log_file , skiprows=2)
        line6, = pl.plot(datatime,dataw,'',label = "w" ,linewidth=1)
if os.path.isfile("e_" + log_file):
        filee.close()
        datae=np.genfromtxt("e_" + log_file , skiprows=2)
        line6, = pl.plot(datatime,datae,'',label = "e" ,linewidth=1)

# plot graphs
pl.legend(handler_map={line1: HandlerLine2D(numpoints=6)}) # plots the legend

pl.title(log_file + "  OpenFOAM - Convergence Plot")
pl.xlabel("Time (s)")
pl.ylabel("Convergence Residual (Log Scale)")

pl.yscale('log')

pl.show()
