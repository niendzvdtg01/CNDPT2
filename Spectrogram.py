import librosa.display
from Load_audio import audio, sr
import matplotlib.pyplot as plt

D = librosa.stft(audio)
S_db = librosa.amplitude_to_db(abs(D))

plt.figure(figsize=(10,4))
librosa.display.specshow(
    S_db, sr=sr,
    x_axis='time',
    y_axis='hz'
)
plt.colorbar()
plt.title("Spectrogram")
plt.show()

#Buoc 3: Phan tich am thanh bang bieu do stft trong thu vien librosa