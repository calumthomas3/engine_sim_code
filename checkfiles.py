# File for storing check function for calling setup if required
import os.path
from Setup import setup
import numpy as np


def check_files(input_files, gear_change_data, min_rpm, max_rpm, rpm_sectioning):
    # Check if the files exist for engine running
    check = []
    file_checkers = np.arange(min_rpm, max_rpm, rpm_sectioning, dtype=int)
    for file_checker in file_checkers:
        check.append(input_files[0][:-8] + str(file_checker) + '_signal.csv')

    for i in range(len(check)):
        if not os.path.isfile(check[i]):
            print('Files not found: ' + str(check[i]))
            print('\nRunning Setup.py')
            setup(input_files, gear_change_data, min_rpm, max_rpm, rpm_sectioning)
            break
        else:
            print('\nFiles found ' + str(i + 1) + '/' + str(len(file_checkers)))

    # Check if gear change data exists
    if not os.path.isfile('geardata.csv'):
        print('Gear Change Data not found')
        print('\nRunning Setup.py')
        setup(input_files, gear_change_data, min_rpm, max_rpm, rpm_sectioning)
    else:
        print('\nGear Change Data found')

    return file_checkers
