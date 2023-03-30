import numpy as np
import keyboard
import sounddevice as sd
from gear_sound_functions import compress_signal
from import_gear_change_data import gear_change_check


# Define the rpm range and corresponding frequency range
rpm_range = np.arange(1000, 3001, 10)
freq_range = np.interp(rpm_range, [1000, 3000], [50, 150])

# Define the sample rate and duration of the signal
sr = 44100
duration = 1000
kRpm = 1000
kSpeedVoltage = 0
kThrottleVoltage = 0


def on_press(key, graphdata, currentgear):
    global kRpm
    if key.name == 'up':
        rpm_load(0.1, 0, graphdata, currentgear)
    elif key.name == 'down':
        rpm_load(-0.1, 0, graphdata, currentgear)
    elif key.name == 'left':
        rpm_load(0, -0.1, graphdata, currentgear)
    elif key.name == 'right':
        rpm_load(0, 0.1, graphdata, currentgear)
    print("Current RPM:", kRpm)


def rpm_load(throttleinput, speedinput, graphdata, currentgear):
    global kThrottleVoltage
    global kSpeedVoltage
    global kRpm
    points = np.array((2, 2))
    points[0, 0] = kThrottleVoltage
    points[0, 1] = kSpeedVoltage
    kThrottleVoltage += throttleinput
    kSpeedVoltage += speedinput
    points[1, 0] = kThrottleVoltage
    points[1, 1] = kSpeedVoltage
    gear_change_check(points, graphdata, currentgear)

    if kRpm > 3000:
        kRpm = 3000
    elif kRpm < 1000:
        kRpm = 1000
    else:
        kRpm = kRpm


# Block Write Method
def output_stream(rpmsignals):
    # Initialize the rpm value to 1000
    global kRpm
    # Set the blocksize to 2048 samples
    block_size = 2048

    # Create an instance of the Stream class
    stream = sd.OutputStream(channels=1, blocksize=block_size)

    # Start the stream
    stream.start()

    print('Playing')

    # Keep writing the signal to the stream until keyboard interrupt
    try:
        while True:
            # Write the signal to the stream in blocks
            for i in range(0, len(rpmsignals[kRpm]), block_size):
                signal_block = rpmsignals[kRpm][i:i + block_size]
                # Change type of signal_block to float32
                signal_block = signal_block.astype('float32')
                stream.write(signal_block)

    except KeyboardInterrupt:
        print('Stopped')
        stream.stop()
        stream.close()


# Callback Method
def output_stream_callback(rpmfreqs):
    start_idx = 0

    try:
        samplerate = 44100

        def callback(outdata, frames, time, status):
            if status:
                print(status, file=sys.stderr)

            t = (start_idx + np.arange(frames)) / samplerate
            global kRpm
            if kRpm == 1000:
                maxpeak = max(rpmfreqs[0][:, 1])
                signal = (rpmfreqs[0][0, 1] / maxpeak) * np.sin(2 * np.pi * rpmfreqs[0][0, 0] * t)
                for i in range(len(rpmfreqs[0]) - 1):
                    signal += (rpmfreqs[0][i + 1, 1] / maxpeak) * np.sin(
                        2 * np.pi * rpmfreqs[0][i + 1, 0] * t)

                # Add some random noise to the signal
                noise = np.random.normal(0, 0.01, len(signal))
                signal += noise

                # Scale the signal to a maximum amplitude of 0.5
                signal *= ((kRpm - 1000) / 1000) / np.max(np.abs(signal))

                # Convert the signal to float32
                outdata[:, 0] = signal.astype('float32')
            elif 1000 < kRpm <= 1500:
                maxpeak = max(rpmfreqs[0][:, 1])
                signal = (rpmfreqs[0][0, 1] / maxpeak) * np.sin(
                    2 * np.pi * (kRpm - 1000)/1000 * rpmfreqs[0][0, 0] * t)
                for i in range(len(rpmfreqs[0]) - 1):
                    signal += (rpmfreqs[0][i + 1, 1] / maxpeak) * np.sin(
                        2 * np.pi * rpmfreqs[0][i + 1, 0] * t)

                # Add some random noise to the signal
                noise = np.random.normal(0, 0.01, len(signal))
                signal += noise

                # Scale the signal to a maximum amplitude of 0.5
                signal *= ((kRpm - 1000) / 1000) / np.max(np.abs(signal))

                # Convert the signal to float32
                outdata[:, 0] = signal.astype('float32')
            elif 1500 < kRpm <= 2000:
                maxpeak = max(rpmfreqs[1][:, 1])
                signal = (rpmfreqs[1][0, 1] / maxpeak) * np.sin(
                    2 * np.pi * (kRpm - 1500) / 1500 * rpmfreqs[1][0, 0] * t)
                for i in range(len(rpmfreqs[1]) - 1):
                    signal += (rpmfreqs[1][i + 1, 1] / maxpeak) * np.sin(
                        2 * np.pi * rpmfreqs[1][i + 1, 0] * t)

                # Add some random noise to the signal
                noise = np.random.normal(0, 0.01, len(signal))
                signal += noise

                # Scale the signal to a maximum amplitude of 0.5
                signal *= ((kRpm - 1000) / 1000) / np.max(np.abs(signal))

                # Convert the signal to float32
                outdata[:, 0] = signal.astype('float32')
            elif 2000 < kRpm <= 2500:
                maxpeak = max(rpmfreqs[2][:, 1])
                signal = (rpmfreqs[2][0, 1] / maxpeak) * np.sin(
                    2 * np.pi * (kRpm - 2000) / 2000 * rpmfreqs[2][0, 0] * t)
                for i in range(len(rpmfreqs[2]) - 1):
                    signal += (rpmfreqs[2][i + 1, 1] / maxpeak) * np.sin(
                        2 * np.pi * rpmfreqs[2][i + 1, 0] * t)

                # Add some random noise to the signal
                noise = np.random.normal(0, 0.01, len(signal))
                signal += noise

                # Scale the signal to a maximum amplitude of 0.5
                signal *= ((kRpm - 1000) / 1000) / np.max(np.abs(signal))

                # Convert the signal to float32
                outdata[:, 0] = signal.astype('float32')
            elif 2500 < kRpm <= 3000:
                maxpeak = max(rpmfreqs[3][:, 1])
                signal = (rpmfreqs[3][0, 1] / maxpeak) * np.sin(
                    2 * np.pi * (kRpm - 2500) / 2500 * rpmfreqs[3][0, 0] * t)
                for i in range(len(rpmfreqs[3]) - 1):
                    signal += (rpmfreqs[3][i + 1, 1] / maxpeak) * np.sin(
                        2 * np.pi * rpmfreqs[3][i + 1, 0] * t)

                # Add some random noise to the signal
                noise = np.random.normal(0, 0.01, len(signal))
                signal += noise

                # Scale the signal to a maximum amplitude of 0.5
                signal *= 2 / np.max(np.abs(signal))

                # Convert the signal to float32
                outdata[:, 0] = signal.astype('float32')
            else:
                maxpeak = max(rpmfreqs[4][:, 1])
                signal = (rpmfreqs[4][0, 1] / maxpeak) * np.sin(
                    2 * np.pi * (kRpm - 3000) / 3000 * rpmfreqs[4][0, 0] * t)
                for i in range(len(rpmfreqs[4]) - 1):
                    signal += (rpmfreqs[4][i + 1, 1] / maxpeak) * np.sin(
                        2 * np.pi * rpmfreqs[4][i + 1, 0] * t)

                # Add some random noise to the signal
                noise = np.random.normal(0, 0.01, len(signal))
                signal += noise

                # Scale the signal to a maximum amplitude of 0.5
                signal *= ((kRpm - 1000) / 1000) / np.max(np.abs(signal))

                # Convert the signal to float32
                outdata[:, 0] = signal.astype('float32')

        with sd.OutputStream(channels=1, callback=callback, samplerate=samplerate) as stream:
            print('Playing')
            print('#' * 80)
            print('press Return to quit')
            print('#' * 80)
            input()
    except KeyboardInterrupt:
        print('Stopped')
        stream.stop()
        stream.close()