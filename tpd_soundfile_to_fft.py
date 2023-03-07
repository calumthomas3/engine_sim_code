import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import find_peaks
import csv


def fft_analysis(filename):
    # Load the Sound File
    samplerate, data = wavfile.read(filename)

    # Set threshold for peaks
    height_threshold = 200

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

    # Find the peaks
    peaks_index, properties = find_peaks(spectrum, height=height_threshold)

    # Use filename
    savefile = filename[:-4]+'_fft.csv'

    # Frequency Output to a csv file
    with open(savefile, 'w', newline='') as file:
        writer = csv.writer(file)
        for i in int(len(peaks_index)):
            writer.writerow(peaks_index[i], properties['peak_heights'][i])
