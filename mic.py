from math import pi, sqrt

import matplotlib.pyplot as plt
import numpy as np
import pyaudio

FORMAT = pyaudio.paFloat32
CHANNELS = 2
RATE = 44100
CHUNK = 2560
RECORD_SECONDS = 1
WAVE_OUTPUT_FILENAME = "out.wav"

SIGMA = 0.5
KERNEL_BASE = np.arange(-50, 50, 1)
KERNEL = np.exp(-KERNEL_BASE ** 2 / (2 * SIGMA ** 2)) / sqrt(pi * 2) / SIGMA
KERNEL -= 0.01
THRESHOLD = 1e-3

audio = pyaudio.PyAudio()

# start Recording
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

plt.show()
while True:
    cur_chunk = np.abs(np.fromstring(stream.read(CHUNK)))
    convolved = np.convolve(KERNEL, cur_chunk)
    if np.max(convolved) > THRESHOLD:
        plt.clf()
        plt.plot(np.convolve(KERNEL, cur_chunk))
        plt.pause(0.0001)

# stop Recording
stream.stop_stream()
stream.close()
audio.terminate()
