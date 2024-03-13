import numpy as np
from scipy.io import wavfile

samplerate = 44100
length = 5
chirplength = 3

f0 = 6000
f1 = 10000

signal = np.arange(chirplength*samplerate)/(chirplength*samplerate)
signal = np.interp(signal, [0, 1], [f0, f1])
signal = np.append(signal, np.repeat(f1, (length-chirplength)*samplerate))
signal = np.sin(signal * 2 * np.pi * np.arange(length*samplerate)/samplerate)
signal = np.float32(signal)
wavfile.write("audio.wav", samplerate, signal)