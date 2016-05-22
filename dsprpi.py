import pyaudio
import numpy as np
import scipy
import sys
import smbus
import time

CHUNK = 1024*2
WIDTH = 2
DTYPE = np.int16
MAX_INT = 32768.0

CHANNELS = 1
RATE = 11025*1
RECORD_SECONDS = 20

j = np.complex(0,1)

p = pyaudio.PyAudio()

stream = p.open(format = p.get_format_from_width(WIDTH), channels = CHANNELS, rate = RATE, input = True, output = True, frames_per_buffer = CHUNK)


print "* recording"

fir = np.zeros(CHUNK*2)
fir[:(2*CHUNK)] = 1.
fir /= fir.sum()

fir_last = fir
avg_freq_buffer = np.zeros(CHUNK)
obj = -np.inf
t = 10

buffer = np.zeros(CHUNK * 2)

while True:
	string_audio_data = stream.read(CHUNK)
	audio_data = np.fromstring(string_audio_data, dtype=DTYPE)
	normalized_data = audio_data / MAX_INT
	freq_data = np.fft.fft(normalized_data)

	if freq_data[0] >= 10:
		print "Bass"
		print freq_data[0]

stream.stop_stream()
stream.close()

p.terminate

