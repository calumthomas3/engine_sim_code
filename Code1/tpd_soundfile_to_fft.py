import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import find_peaks
import pandas as pd


def fft_analysis(filename):
    # Load the Sound File
    samplerate, data = wavfile.read(filename)

    # Normalise the data to the range (-1, 1)
    data = data / (2**15)

    # Calculate FFT
    spectrum = np.abs(np.fft.rfft(data))
    frequencies = np.fft.rfftfreq(len(data), d=1/samplerate)

    # Plot the Spectrum
    plt.plot(frequencies, spectrum)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Occurence')
    plt.xlim(0, 5000)
    plt.title('FFT of Sound File '+str(filename))
    plt.show()

    height_threshold = max(spectrum) * 0.05
    # Filter the data
    filter_array = np.where(spectrum >= height_threshold)
    spectrum = spectrum[filter_array]
    frequencies = frequencies[filter_array]
    filter_array = np.where(frequencies <= 5000)
    spectrum = spectrum[filter_array]
    frequencies = frequencies[filter_array]

    # Store Data
    data = {'Peak Freq': frequencies, 'Heights': spectrum}

    # Use filename
    savefile = filename[:-4]+'_fft.csv'
    df = pd.DataFrame(data)
    pd.DataFrame(df).to_csv(savefile, index=False, header=False)
    print(df)
    return savefile


# Create Files for each RPM
def stream_signals(frequency_files, min_rpm, max_rpm, rpm_sectioning):
    rpm_values = {}
    rpm_signals = {}

    # Define the sample rate and duration of the signal
    sr = 44100
    duration = 100

    for i in range(len(frequency_files)):
        df = pd.read_csv(frequency_files[i], header=None)
        rpm_values[i] = df.values
        print(rpm_values[i])

    # Create a time array from 0 to the duration with a step size of 1/sr
    t = np.arange(0, duration, 1 / sr)
    created_rpms = np.arange(min_rpm, max_rpm, rpm_sectioning, dtype=int)

    # Add other  to the signal
    for created_rpm in created_rpms:
        if created_rpm <= 1500:
            signal = synth_sound_files(created_rpm, rpm_values[0], rpm_values[1], t)

        elif 1500 < created_rpm <= 2000:
            signal = synth_sound_files(created_rpm, rpm_values[1], rpm_values[2], t)

        elif 2000 < created_rpm <= 2500:
            signal = synth_sound_files(created_rpm, rpm_values[2], rpm_values[3], t)

        elif 2500 < created_rpm <= 3000:
            signal = synth_sound_files(created_rpm, rpm_values[3], rpm_values[4], t)

        # Save the signal to a file

        savefile = frequency_files[0][:-12] + str(created_rpm) + '_signal.csv'

        print('\nFile Created: ' + str(savefile))

        pd.DataFrame(signal).to_csv(savefile, index=False, header=False)


def synth_sound_files(created_rpm, rpm_1, rpm_2, t):
    maxpeak1 = max(rpm_1[:, 1])
    maxpeak2 = max(rpm_2[:, 1])
    signal = (rpm_1[0, 1] / maxpeak1) * \
        ((1500 - created_rpm) / 500) * \
        np.sin(2 * np.pi * (created_rpm / 1000) * rpm_1[0, 0] * t)
    signal += (rpm_2[0, 1] / maxpeak2) * \
        ((created_rpm - 1000) / 500) * \
        np.sin(2 * np.pi * (created_rpm / 1500) * rpm_2[0, 0] * t)

    for i in range(len(rpm_1) - 1):
        signal += (rpm_1[i+1, 1] / (((i + 1)/10) * maxpeak1)) * \
            ((1500 - created_rpm) / 500) * \
            np.sin(2 * np.pi * (created_rpm / 1000) * rpm_1[i+1, 0] * t)
    for i in range(len(rpm_2) - 1):
        signal += (rpm_2[0, 1] / (((i + 1)/10) * maxpeak2)) * \
            ((created_rpm - 1000) / 500) * \
            np.sin(2 * np.pi * (created_rpm / 1500) * rpm_2[i+1, 0] * t)

    # Add some random noise to the signal
    noise = np.random.normal(0, 0.01, len(signal))
    signal += noise

    # Remove initial peak noise
    signal = signal[-1000:]

    # Scale the signal to a maximum amplitude of 0.5
    signal *= 0.75 / np.max(np.abs(signal))

    # Convert the signal to float32
    signal = signal.astype('float32')

    return signal
