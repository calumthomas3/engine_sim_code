import os.path
from Setup import setup
import pandas as pd
from play_gear_sound import output_stream, on_press
import keyboard

# Define the input files and the gear change data
input_files = ('sound_files/front_1000.wav',
               'sound_files/front_1500.wav',
               'sound_files/front_2000.wav',
               'sound_files/front_2500.wav',
               'sound_files/front_3000.wav'
               )
gear_change_data = '2D_gear_change_profile.xlsx'

# Check if the files exist for engine running
check = []
for i in range(len(input_files)):
    check.append(input_files[i][:-4]+'_signal.csv')

for i in range(len(input_files)):
    if not os.path.isfile(check[i]):
        print('Files not found: '+str(check[i]))
        print('\nRunning Setup.py')
        setup(input_files, gear_change_data)
        break
    else:
        print('\nFiles found '+str(i)+'/'+str(len(input_files)))

# Run the engine
print('\nRunning Engine')

rpm_signals = []
for i in range(len(input_files)):
    rpm_signals.append(pd.read_csv(check[i], header=None).values.flatten())
# Initialize the rpm value to 1000
kRpm = 1000
# Register the callback function with the keyboard module
keyboard.on_press(on_press)
# Output the signals to the rpm stream
output_stream(rpm_signals)
