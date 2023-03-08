from tpd_soundfile_to_fft import fft_analysis, stream_signals
from import_gear_change_data import import_gear_change, gear_change_graph
import sounddevice


def setup(input_files, gear_change_data):

    devices = sounddevice.query_devices(device=None, kind=None)
    print(devices)

    ulines_dir, dlines_dir = import_gear_change(gear_change_data)

    savefiles = []

    for i in range(len(input_files)):
        savefile = fft_analysis(input_files[i])
        savefiles.append(savefile)

    print('\nFiles saved')

    # gear_change_graph(ulines_dir, dlines_dir)

    # Set the signals for each rpm to be stretched and changed in the rpm stream
    stream_signals(savefiles)

    print('\nAll rpm_signals created')