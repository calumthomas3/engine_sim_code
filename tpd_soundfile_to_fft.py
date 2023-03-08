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

    height_threshold = max(spectrum) * 0.1

    # Find the peaks
    peaks_index, properties = find_peaks(spectrum, height=height_threshold)

    # Use filename
    savefile = filename[:-4]+'_fft.csv'

    pd.DataFrame(peaks_index).to_csv(savefile, index=False, header=False)

    return savefile


# Increase or Decrease RPM
def stream_signals(frequency_files):
    rpm_values = {}
    rpm_signals = {}

    # Define the sample rate and duration of the signal
    sr = 44100
    duration = 100

    for i in range(len(frequency_files)):
        df = pd.read_csv(frequency_files[i], header=None)
        rpm_values[i] = df[0].values

    # Create a time array from 0 to the duration with a step size of 1/sr
    t = np.arange(0, duration, 1 / sr)

    # Add other  to the signal
    for rpm_value in rpm_values:
        signal = np.sin(2 * np.pi * rpm_values[rpm_value][0] * t)
        for i in range(len(rpm_values[rpm_value]) - 1):
            signal += (1/(i+1)) * np.sin(2 * np.pi * rpm_values[rpm_value][i + 1] * t)

        # Add some random noise to the signal
        noise = np.random.normal(0, 0.1, len(signal))
        signal += noise

        # Scale the signal to a maximum amplitude of 0.5
        signal *= 1 / np.max(np.abs(signal))

        # Convert the signal to float32
        signal = signal.astype('float32')

        # Save the signal to an array dictionary
        rpm_signals[rpm_value] = signal

        savefile = frequency_files[rpm_value][:-8] + '_signal.csv'

        print('\nFile Created: ' + str(savefile))

        pd.DataFrame(signal).to_csv(savefile, index=False, header=False)
