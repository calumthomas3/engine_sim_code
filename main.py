from tpd_soundfile_to_fft import fft_analysis
from import_gear_change_data import import_gear_change, gear_change_graph
import sounddevice
from play_gear_sound import output_stream, stream_signals

devices = sounddevice.query_devices(device=None, kind=None)
print(devices)

input_files = ('sound_files/front_1000.wav',
               'sound_files/front_1500.wav',
               'sound_files/front_2000.wav',
               'sound_files/front_2500.wav',
               'sound_files/front_3000.wav'
               )
gear_change_data = '2D_gear_change_profile.xlsx'

ulines_dir, dlines_dir = import_gear_change(gear_change_data)

savefiles = []

for i in range(len(input_files)):
    savefile = fft_analysis(input_files[i])
    savefiles.append(savefile)

# gear_change_graph(ulines_dir, dlines_dir)

# Set the signals for each rpm to be stretched and changed in the rpm stream
rpm_signals = stream_signals(savefiles)

print(rpm_signals)

# Output the signals to the rpm stream
output_stream(rpm_signals)
