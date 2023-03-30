import numpy as np
import math

import time
import threading


bits = 16
sample_rate = 44100

def sine_x(amp, freq, t):
    return int(round(amp * math.sin(2 * math.pi * freq * time)))


class Tone:
    def sine(freq, duration=10, speaker=None):

        num_samples = int(round(duration*sample_rate))

        sound_buffer = np.zeros((num_samples, 2), dtype=np.int16)

        amplitude = 2**(bits-1) -1

        for sample_num in range(num_samples):
            t = float(sample_num)/sample_rate

            sine = sine_x(amplitude, freq, t)

            if speaker == 'r':
                sound_buffer[sample_num][1] = sine
            if speaker == 'l':
                sound_buffer[sample_num][0] = sine

            else:
                sound_buffer[sample_num][0] = sine
                sound_buffer[sample_num][1] = sine

        sound = pygame.sndarray.make_sound(sound_buffer)
        sound.play(loops=-1)

        time.sleep(duration)

    @staticmethod
    def engine_from_list(freq_list, duration=10, speaker=None):
        engine_threads = []
        for freq in freq_list:
            engine_thread = threading.Thread(target=Tone.sine, args=[freq, duration, speaker])
            engine_threads.append(engine_thread)

        for engine_thread in engine_threads:
            engine_thread.start()

        for engine_thread in engine_threads:
            engine_thread.join()
