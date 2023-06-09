import numpy as np
import matplotlib.pyplot as plt
import pydub
from scipy.io import wavfile
from scipy.signal import find_peaks
import pandas as pd


def match_target_amplitude(sound, target_dBFS):
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)


# Create Files for each RPM
def create_sounds(sound_files, min_rpm, max_rpm, rpm_sectioning):
    created_rpms = np.arange(min_rpm, max_rpm + 5, rpm_sectioning)

    # Add other  to the signal
    for created_rpm in created_rpms:
        if created_rpm <= 1500:
            synth_sound_files(created_rpm, sound_files[0], sound_files[1])

        elif 1500 < created_rpm <= 2000:
            synth_sound_files(created_rpm, sound_files[1], sound_files[2])

        elif 2000 < created_rpm <= 2500:
            synth_sound_files(created_rpm, sound_files[2], sound_files[3])

        elif 2500 < created_rpm <= 3000:
            synth_sound_files(created_rpm, sound_files[3], sound_files[4])

        else:
            synth_sound_files(created_rpm, sound_files[4], sound_files[4])


def synth_sound_files(created_rpm, rpm_1, rpm_2):
    low_val = int(rpm_1[17:-4])
    high_val = int(rpm_2[17:-4])
    rpm_low = pydub.AudioSegment.from_file(rpm_1, format="wav")
    rpm_high = pydub.AudioSegment.from_file(rpm_2, format="wav")

    # Speed up/Slow Down Audio samples
    rpm_low.speedup(playback_speed=(created_rpm / low_val))
    rpm_high.speedup(playback_speed=(created_rpm / high_val))

    # Increase Volume across rpm
    low_change_dB = (high_val - created_rpm) / 100
    high_change_dB = (created_rpm - low_val) / 100

    rpm_low = match_target_amplitude(rpm_low, -10 + low_change_dB)
    rpm_high = match_target_amplitude(rpm_high, -10 + high_change_dB)

    # Take first three seconds of the audio
    rpm_low = rpm_low[500:2500]
    rpm_high = rpm_high[500:2500]

    # Add signal together
    signal = rpm_low.overlay(rpm_high)



    # Save the signal to a file

    savefile = 'sound_files/' + str(created_rpm) + '_sound.wav'

    print('\nFile Created: ' + str(savefile))

    signal.export(savefile, format="wav")
