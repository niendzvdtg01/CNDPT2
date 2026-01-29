from scipy.signal import butter, filtfilt
from Load_audio import audio, sr

def lowpass(data, cutoff, sr):
    nyq = 0.5 * sr
    normal = cutoff / nyq
    b, a = butter(5, normal, btype="low")
    return filtfilt(b, a, data)

filtered = lowpass(audio, 4000, sr)

#Buoc 4 thuc hien giam am thanh