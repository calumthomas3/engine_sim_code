from tpd_soundfile_to_fft import fft_analysis
from import_gear_change_data import import_gear_change, gear_change_graph
import sounddevice
# from sine import Tone

# devices = sounddevice.query_devices(device=None, kind=None)
# print(devices)

input_files = (
    'sound_files/front_1000.wav',
    'sound_files/front_1500.wav',
    'sound_files/front_2000.wav',
    'sound_files/front_2500.wav',
    'sound_files/front_3000.wav'
)
gear_change_data = '2D_gear_change_profile.xlsx'

ulines_dir, dlines_dir = import_gear_change(gear_change_data)

for input_file in input_files:
    fft_analysis(input_file)

# gear_change_graph(ulines_dir, dlines_dir)


# def on_press(key):
    # global freq
    # global rpm
    # if key.name == 'up':
        # freq_idx = np.searchsorted(freq_range, freq)
        # freq = freq_range[min(freq_idx + 1, len(freq_range) - 1)]
        # rpm = int(np.interp(freq, freq_range, rpm_range))
    # elif key.name == 'down':
        # freq_idx = np.searchsorted(freq_range, freq)
        # freq = freq_range[max(freq_idx - 1, 0)]
        # rpm = int(np.interp(freq, freq_range, rpm_range))
    # print("Current RPM:", rpm)

#Tone.engine_from_list(prom_freqs)
