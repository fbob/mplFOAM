#!/usr/bin/env python

import os
import subprocess
import sys

# Cases names (list of directories):
cases_names = ["pitzDaily1","pitzDaily2","pitzDaily3"]

# Run in parallel
parallel = True # Or False for one proc

# Redirect the output of the Python script to a file
log_filename ="runCases.log"
log_file = open(log_filename, 'w')
sys.stdout = log_file

# Ensure that all cases (directories) exist and remove the non-existent ones from the list.
cases_names_exist = cases_names.copy()
for case_name in cases_names:
    if not os.path.isdir(case_name):
        print("Warning: The case directory " + case_name + " does not exist.")
        cases_names_exist.remove(case_name)
if len(cases_names_exist) == 0:
     print("Error: No case found")
     sys.exit()

# Start the main loop on case directory
# If you don't want to wait for the end of the foamJob process
# please remove the '-wait' option
for case_name in cases_names_exist:
    # Change to the case directory.
    os.chdir("./" + case_name)
    print("===========================", flush=True)
    print("Working in case directory: " + case_name, flush=True)
    print("===========================", flush=True)
    if parallel:
        # Decompose the case: output in 'log.decomposePar' file
        subprocess.call("decomposePar 2>&1 | tee -a log.decomposePar",
                        shell=True,
                        stdout=log_file,
                        stderr=subprocess.STDOUT)
        # Run the OpenFoam case in parallel: output in 'log' file
        subprocess.call("foamJob -wait -p simpleFoam",
                        shell=True,
                        stdout=log_file,
                        stderr=subprocess.STDOUT)
        # Reconstruct the case: output in 'log.reconstructPar' file
        subprocess.call("reconstructPar -latestTime 2>&1 | tee -a log.reconstructPar",
                        shell=True,
                        stdout=log_file,
                        stderr=subprocess.STDOUT)
    else:
        # Run the OpenFoam case
        subprocess.call("foamJob -wait simpleFoam",
                        shell=True,
                        stdout=log_file,
                        stderr=subprocess.STDOUT)
    # Revert to the root directory.
    os.chdir("../")
