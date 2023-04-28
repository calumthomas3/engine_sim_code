import numpy as np
import matplotlib.pyplot as plt
import pydub
from scipy.io import wavfile
from scipy.signal import find_peaks
import pandas as pd


# Create Files for each RPM
def create_sounds(sound_files, min_rpm, max_rpm, rpm_sectioning):
    created_rpms = np.arange(min_rpm, max_rpm + 5, rpm_sectioning)

    # Add other  to the signal
    for created_rpm in created_rpms:
        synth_sound_files(created_rpm, sound_files)


def synth_sound_files(created_rpm, sound_files):
    val = np.array(len(sound_files))
    i = 0
    for sound_file in sound_files:
        val[i] = int(sound_file[18:-4])
        i += 1

    signal = pydub.AudioSegment.empty()
    i = 0
    for sound_file in sound_files:
        x = pydub.AudioSegment.from_file(sound_file, format="wav")

        # Speed up/Slow Down Audio samples
        x.speedup(playback_speed=(created_rpm/val[i]))

        # Increase Volume across rpm
        diff = abs(created_rpm - val[i])
        if diff == 0:
            x = x + 10
        else:
            x = x + 10/diff

        x = x[500:2500]

        signal += x

        i += 1

    # Save the signal to a file
    savefile = 'sound_files/' + str(created_rpm) + '_sound.wav'

    print('\nFile Created: ' + str(savefile))

    signal.export(savefile, format="wav")
