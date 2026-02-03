import librosa
import numpy as np
import os


def load_processed_audio(file_path):
    if not os.path.exists(file_path):
        print(f"Lỗi: Không tìm thấy file tại {file_path}")
        return None, None

    # 1. Load audio giữ nguyên sample rate gốc
    # mono=True giúp đưa về 1 kênh để dễ dàng xử lý toán học phía sau
    audio, sr = librosa.load(file_path, sr=None, mono=True)

    # 2. Chuẩn hóa biên độ (Peak Normalization)
    # Giúp tín hiệu không bị quá bé hoặc quá lớn (clipping)
    if np.max(np.abs(audio)) > 0:
        audio = audio / np.max(np.abs(audio))

    return audio, sr


# Thực hiện load file để các module khác (FFT, Spectrogram) sử dụng
path = "./input.wav"
audio, sr = load_processed_audio(path)

if audio is not None:
    print(f"--- Thông số file đầu vào ---")
    print(f"Sample rate: {sr} Hz")
    print(f"Độ dài: {len(audio) / sr:.2f} giây")
    print(f"Số lượng mẫu: {len(audio)}")
