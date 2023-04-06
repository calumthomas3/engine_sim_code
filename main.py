# Main file for the engine simulation
import pandas as pd
from play_gear_sound import output_stream, on_press
import keyboard
from joystick import joystick_init, joystick_check
from checkfiles import check_files


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

# Block Write Method
# Check if the files exist for engine running
file_checkers = check_files(input_files, gear_change_data, min_rpm, max_rpm, rpm_sectioning)

# Set Up the engine
print('\nSet Up Engine')

# Initialise Inputs
joystick_init()

rpm_signals = {}
for i in range(len(file_checkers)):
    file_checker = file_checkers[i]
    rpm_signals[file_checker] = pd.read_csv(file_checkers[i], header=None).values.flatten()
graphdata = pd.read_csv('geardata.csv')

# Initialize voltages to 0, gear to 1, and the rpm value to 1000
voltage = 0
speed = 0
kRpm = 1000
currentgear = 1

# Run the engine
print('\nRunning Engine')

# Keyboard input
# keyboard.on_press(on_press, graphdata, currentgear)
# Controller input
joystick_check()

# Output the signals to the rpm stream
output_stream(rpm_signals)
