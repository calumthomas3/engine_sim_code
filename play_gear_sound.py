import numpy as np
import pandas as pd
import sounddevice as sd
import keyboard


# Increase or Decrease RPM
def on_press(key, freq_range, rpm_range):
    global freq
    global rpm
    if key.name == 'up':
        freq_idx = np.searchsorted(freq_range, freq)
        freq = freq_range[min(freq_idx+1, len(freq_range)-1)]
        rpm = int(np.interp(freq, freq_range, rpm_range))
    elif key.name == 'down':
        freq_idx = np.searchsorted(freq_range, freq)
        freq = freq_range[max(freq_idx-1, 0)]
        rpm = int(np.interp(freq, freq_range, rpm_range))
    print("Current RPM:", rpm)


def stream_signals(frequency_files):
    rpm_values = {}
    rpm_signals = {}
    for i in range(len(frequency_files)):
        df = pd.read_csv(frequency_files[i], header=None)
        rpm_values[i] = df[0].values

    # Define the sample rate and duration of the signal
    sr = 44100
    duration = 10

    # Create a time array from 0 to the duration with a step size of 1/sr
    t = np.arange(0, duration, 1 / sr)

    # Add harmonics to the signal
    for rpm_value in rpm_values:
        signal = np.sin(2 * np.pi * rpm_values[rpm_value][0] * t)
        for i in range(len(rpm_values[rpm_value]) - 1):
            signal += (1 / (i + 4)) * np.sin(2 * np.pi * rpm_values[rpm_value][i + 1] * t)

        # Add some random noise to the signal
        noise = np.random.normal(0, 0.1, len(signal))
        signal += noise

        # Scale the signal to a maximum amplitude of 0.5
        signal *= 0.5 / np.max(np.abs(signal))

        # Convert the signal to float32
        signal = signal.astype('float32')

        # Save the signal to an array dictionary
        rpm_signals[rpm_value] = signal

    return rpm_signals


def output_stream(rpm_signals):
    # Define the rpm range and corresponding frequency range
    rpm_range = np.arange(1000, 3001, 10)
    freq_range = np.interp(rpm_range, [1000, 3000], [50, 150])

    # Set the blocksize to 2048 samples
    block_size = 2048

    # Create an instance of the Stream class
    stream = sd.OutputStream(channels=2, blocksize=block_size)

    # Keyboard Interaction
    keyboard.on_press(on_press, freq_range, rpm_range)

    # Start the stream
    stream.start()

    # Initialize the rpm value to 1000
    rpm_idle = 1000
    rpm = rpm_idle
    # Keep writing the signal to the stream until keyboard interrupt
    try:
        while True:
            # Write the signal to the stream in blocks
            if rpm <= 1000:
                rpm = rpm_idle
                for i in range(0, len(rpm_signals[0]), block_size):
                    sin_signal = np.squeeze(np.sin(2 * np.pi * rpm_signals[0][0] * np.arange(block_size) / sr))
                    signal_block = rpm_signals[0][i:i + block_size]
                    # Modify the frequency of the sine wave
                    signal_block *= sin_signal
                    stream.write(signal_block)
                    # Print the current rpm value
                    print(f"Current RPM: {rpm}", end='\r')
            if rpm > 1000 and rpm <= 1500:
                # Form two channel sound input
                input = [rpm_signals[0] * (rpm/1000), rpm_signals[1] * (rpm/1500)]
                for i in range(0, len(rpm_signals[0]), block_size):
                    # Generate the sin wave array with length of the block size and remove the extra dimension
                    sin_signal = np.squeeze(np.sin(2 * np.pi * input * np.arange(block_size) / sr))
                    # Modify the frequency of the sine wave
                    signal_block *= sin_signal
                    stream.write(input)
                    # Print the current rpm value
                    print(f"Current RPM: {rpm}", end='\r')

    except KeyboardInterrupt:
        stream.stop()
        keyboard.unhook_all()