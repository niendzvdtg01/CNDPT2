import numpy as np
import librosa
import soundfile as sf
from scipy.signal import butter, filtfilt
import os
from Load_audio import audio, sr


def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def apply_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    return filtfilt(b, a, data)


if __name__ == "__main__":
    if not os.path.exists('Results'): os.makedirs('Results')

    # Lọc dải tần 300Hz - 4000Hz để loại bỏ ù và rít
    # Đây là dải tần tối ưu cho giọng nói trong Podcast/Phỏng vấn
    filtered_bp = apply_bandpass_filter(audio, 300, 4000, sr)

    # Lưu file trung gian vào Results
    sf.write("Results/temp_bandpass.wav", filtered_bp, sr)
    print("--- Bước 1: Đã lọc Band-pass và lưu file trung gian ---")
