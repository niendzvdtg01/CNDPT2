import noisereduce as nr
from Low_pass_filter import filtered
from Load_audio import sr, audio
import soundfile as sf
import matplotlib.pyplot as plt

clean = nr.reduce_noise(
    y=filtered,
    sr=sr,
    prop_decrease=0.8
)

sf.write("output.wav", clean, sr)

plt.plot(audio, alpha=0.5, label="Original")
plt.plot(clean, label="Filtered")
plt.legend()
plt.show()

#Buoc cuoi:Giam am thanh bang noisereduce
