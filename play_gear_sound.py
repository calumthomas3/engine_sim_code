import numpy as np
import keyboard
import sounddevice as sd


# Define the rpm range and corresponding frequency range
rpm_range = np.arange(1000, 3001, 10)
freq_range = np.interp(rpm_range, [1000, 3000], [50, 150])

# Define the sample rate and duration of the signal
sr = 44100
duration = 1000
kRpm = 1000

def on_press(key):
    global kRpm
    if key.name == 'up':
        rpm_load(5)
    elif key.name == 'down':
        rpm_load(-5)
    print("Current RPM:", kRpm)


def rpm_load(rpmInt):
    global kRpm
    kRpm += rpmInt
    if kRpm > 3000:
        kRpm = 3000
    elif kRpm < 1000:
        kRpm = 1000
    else:
        kRpm = kRpm


def output_stream(rpmsignals):
    # Initialize the rpm value to 1000
    global kRpm
    # Set the blocksize to 2048 samples
    block_size = 2048

    # Create an instance of the Stream class
    stream = sd.OutputStream(channels=1, blocksize=block_size)

    # Use base frequency of 1000 rpm
    freq = rpmsignals[0][0]

    # Start the stream
    stream.start()

    print('Playing')

    # Keep writing the signal to the stream until keyboard interrupt
    try:
        while True:
            # Write the signal to the stream in blocks
            if kRpm <= 1000:
                for i in range(0, len(rpmsignals[0]), block_size):
                    sin_signal = np.squeeze(np.sin(2 * np.pi * rpmsignals[0][i] * np.arange(block_size) / sr))
                    signal_block = rpmsignals[0][i:i + block_size]
                    # Modify the frequency of the sine wave
                    signal_block *= sin_signal
                    # Change type of signal_block to float32
                    signal_block = signal_block.astype('float32')
                    stream.write(signal_block)
                    # Print the current rpm value
                    print(f"Current RPM: {kRpm}", end='\r')
            elif 1000 < kRpm <= 1500:
                # Form two channel sound input
                input1 = rpmsignals[0] * ((1500-kRpm)/500)
                input2 = rpmsignals[1] * ((kRpm-1000)/500)
                for i in range(0, len(rpmsignals[0]), block_size):
                    # Generate the sin wave array with length of the block size and remove the extra dimension
                    sin_signal1 = np.squeeze(np.sin(2 * np.pi * input1[i] * np.arange(block_size) / sr))
                    sin_signal2 = np.squeeze(np.sin(2 * np.pi * input2[i] * np.arange(block_size) / sr))
                    sin_signal = sin_signal1 + sin_signal2
                    signal_block = rpmsignals[0][i:i + block_size]
                    # Modify the frequency of the sine wave
                    signal_block *= sin_signal
                    stream.write(input)
                    # Print the current rpm value
                    print(f"Current RPM: {kRpm}", end='\r')
    except KeyboardInterrupt:
        print('Stopped')
        stream.stop()
        stream.close()