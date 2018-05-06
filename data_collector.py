import os
import wave
from math import pi, sqrt
from uuid import uuid4

import matplotlib.pyplot as plt
import numpy as np
import pyaudio

FORMAT = pyaudio.paFloat32
CHANNELS = 2
RATE = 44100
CHUNK = 256
RECORD_TIME = 0.5

SIGMA = 0.5
KERNEL_BASE = np.arange(-50, 50, 1)
KERNEL = np.exp(-KERNEL_BASE ** 2 / (2 * SIGMA ** 2)) / sqrt(pi * 2) / SIGMA
KERNEL -= 0.01
THRESHOLD = 1e-3

clap = False

if not os.path.exists('data'):
    os.mkdir('data')

for i in range(300):
    print("Recording " + ("clap" if clap else "noise") + "...")
    audio = pyaudio.PyAudio()

    # start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    frames = []
    for i in range(int(RATE / CHUNK * RECORD_TIME)):
        frames.append(np.fromstring(stream.read(CHUNK)))

    frames = np.concatenate(frames)
    if clap:
        np.save('data/' + str(uuid4()) + '-clap.npy', frames)
    else:
        np.save('data/' + str(uuid4()) + '-noise.npy', frames)

    if i == 150:
        clap = not clap
    
    stream.stop_stream()
    stream.close()

audio.terminate()

plt.plot(frames)
plt.show()
