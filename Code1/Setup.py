# Import packages
import sounddevice
# Import Functions
from Code1.tpd_soundfile_to_fft import fft_analysis, stream_signals


def setup(input_files, gear_change_data, min_rpm, max_rpm, rpm_sectioning):

    devices = sounddevice.query_devices(device=None, kind=None)
    print(devices)

    savefiles = []

    for i in range(len(input_files)):
        savefile = fft_analysis(input_files[i])
        savefiles.append(savefile)

    print('\nFiles saved')

    # Set the signals for each rpm for section
    stream_signals(savefiles, min_rpm, max_rpm, rpm_sectioning)

    print('\nAll rpm_signals created')