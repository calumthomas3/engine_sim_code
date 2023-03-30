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
