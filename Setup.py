from tpd_soundfile_to_fft import fft_analysis, stream_signals, synth_sound_files
from import_gear_change_data import import_gear_change, gear_change_graph
import sounddevice
import pandas as pd


def setup(input_files, gear_change_data, min_rpm, max_rpm, rpm_sectioning):

    devices = sounddevice.query_devices(device=None, kind=None)
    print(devices)

    ulines_dir, dlines_dir = import_gear_change(gear_change_data)

    savefiles = []

    for i in range(len(input_files)):
        savefile = fft_analysis(input_files[i])
        savefiles.append(savefile)

    print('\nFiles saved')

    graphdata = gear_change_graph(ulines_dir, dlines_dir)

    # Write graphdata to csv file
    pd.DataFrame(graphdata).to_csv('geardata.csv', index=False, header=False)

    # Set the signals for each rpm for section
    stream_signals(savefiles, min_rpm, max_rpm, rpm_sectioning)

    print('\nAll rpm_signals created')