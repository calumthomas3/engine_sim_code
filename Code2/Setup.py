# Import packages
import sounddevice
import pandas as pd
# Import Functions
from Code2.create_sounds import create_sounds
from Code2.Functions import ImportFunctions, GearFunctions


def setup(input_files, gear_change_data, min_rpm, max_rpm, rpm_sectioning):

    devices = sounddevice.query_devices(device=None, kind=None)
    print(devices)

    print('\nFiles saved')

    # Set the signals for each rpm for section
    create_sounds(input_files, min_rpm, max_rpm, rpm_sectioning)

    print('\nAll rpm_signals created')