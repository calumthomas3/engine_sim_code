import os.path
from Setup import setup
import pandas as pd
from play_gear_sound import output_stream, output_stream_callback, on_press
import keyboard
import numpy as np

# Define the input files and the gear change data
input_files = ('sound_files/front_1000.wav',
               'sound_files/front_1500.wav',
               'sound_files/front_2000.wav',
               'sound_files/front_2500.wav',
               'sound_files/front_3000.wav'
               )

# Import Gear Change Data
gear_change_data = '2D_gear_change_profile.xlsx'

# Set the number of rpm sections
min_rpm = 1000
max_rpm = 3000
rpm_sectioning = 5
file_checkers = np.arange(min_rpm, max_rpm, rpm_sectioning, dtype=int)

# Block Write Method
# Check if the files exist for engine running
check = []
for file_checker in file_checkers:
    check.append(input_files[0][:-8] + str(file_checker) + '_signal.csv')

for i in range(len(check)):
    if not os.path.isfile(check[i]):
        print('Files not found: '+str(check[i]))
        print('\nRunning Setup.py')
        setup(input_files, gear_change_data, min_rpm, max_rpm, rpm_sectioning)
        break
    else:
        print('\nFiles found '+str(i+1)+'/'+str(len(file_checkers)))

# Check if gear change data exists
if not os.path.isfile('geardata.csv'):
    print('Gear Change Data not found')
    print('\nRunning Setup.py')
    setup(input_files, gear_change_data, min_rpm, max_rpm, rpm_sectioning)
else:
    print('\nGear Change Data found')

# Run the engine
print('\nRunning Engine')

rpm_signals = {}
for i in range(len(check)):
    file_checker = file_checkers[i]
    rpm_signals[file_checker] = pd.read_csv(check[i], header=None).values.flatten()
graphdata = pd.read_csv('geardata.csv')

# Initialize voltages to 0, gear to 1, and the rpm value to 1000
voltage = 0
speed = 0
kRpm = 1000
currentgear = 1

# Run the engine
print('\nRunning Engine')

# Register the callback function with the keyboard module
keyboard.on_press(on_press, graphdata, currentgear)

# Output the signals to the rpm stream
output_stream(rpm_signals)


# # Callback Method
# # Check if the files exist for engine running
# check = []
# for i in range(len(input_files)):
#     check.append(input_files[i][:-4]+'_fft.csv')
#
# for i in range(len(input_files)):
#     if not os.path.isfile(check[i]):
#         print('Files not found: '+str(check[i]))
#         print('\nRunning Setup.py')
#         setup(input_files, gear_change_data)
#         break
#     else:
#         print('\nFiles found '+str(i+1)+'/'+str(len(input_files)))
#
# # Run the engine
# print('\nRunning Engine')
#
# rpm_signals = []
# for i in range(len(input_files)):
#     rpm_signals.append(pd.read_csv(check[i], header=None).values)
# # Initialize the rpm value to 1000
# kRpm = 1000
# # Register the callback function with the keyboard module
# keyboard.on_press(on_press)
# # Output the signals to the rpm stream
# output_stream_callback(rpm_signals)