import numpy as np
import sounddevice as sd
import keyboard
import threading
from sine import Tone

# Increase or Decrease RPM
def on_press(key):
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


class Engine:
    def play(self, speaker=None):
        Tone.sine(self.freq, duration=self.duration)

    @staticmethod
    def rest(duration):
        time.sleep(duration)

    @staticmethod
    def play_enginesound(freq_list):
        freq_threads= []

        for frequency in freq_list:
            freq_thread = threading.Thread(target=engine.play)
            freq_threads.append(freq_thread)

        for freq_thread in freq_threads:
            freq_thread.start()

        for freq_thread in freq_threads:
            freq_thread.join()
