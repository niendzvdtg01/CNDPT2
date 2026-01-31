import numpy as np
import matplotlib.pyplot as plt
from Load_audio import  audio, sr

fft = np.fft.fft(audio)
freq = np.fft.fftfreq(len(fft), 1/sr)

plt.plot(freq[:len(freq)//2],
         np.abs(fft[:len(freq)//2]))
plt.title("FFT Spectrum")
plt.xlabel("Frequency")
plt.ylabel("Magnitude")
plt.show()

#Buoc 2 Phan tich file am thanh bang bieu do fft

